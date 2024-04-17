import pyaudio
import argparse
import asyncio
import json
import os
import sys
import websockets
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from datetime import datetime
from utils.deepgram_argparser import parse_args
startTime = datetime.now()

all_mic_data = []
all_transcripts = []

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 8000

audio_queue = asyncio.Queue()

# Mimic sending a real-time stream by sending this many seconds of audio at a time.
# Used for file "streaming" only.
REALTIME_RESOLUTION = 0.250

def add_whitespace(all_transcripts):
    for i in range(1, len(all_transcripts)):
        all_transcripts[i] = ' ' + all_transcripts[i]
    return all_transcripts

# Used for microphone streaming only.
def mic_callback(input_data, frame_count, time_info, status_flag):
    audio_queue.put_nowait(input_data)
    return (input_data, pyaudio.paContinue)


async def run(key, method, format, **kwargs):
    deepgram_url = f'{kwargs["host"]}/v1/listen?punctuate=true'
    STOP_WORDS = ['next', 'next?', 'goodbye']

    if kwargs["model"]:
        deepgram_url += f"&model={kwargs['model']}"

    if kwargs["tier"]:
        deepgram_url += f"&tier={kwargs['tier']}"

    if method == "mic":
        deepgram_url += "&encoding=linear16&sample_rate=16000"
    else:
        raise Exception("Did you mispell mic?")

    # Connect to the real-time streaming endpoint, attaching our credentials.
    async with websockets.connect(
        deepgram_url, extra_headers={"Authorization": "Token {}".format(key)}
    ) as ws:
        print(f'ℹ️  Request ID: {ws.response_headers.get("dg-request-id")}')
        if kwargs["model"]:
            print(f'ℹ️  Model: {kwargs["model"]}')
        if kwargs["tier"]:
            print(f'ℹ️  Tier: {kwargs["tier"]}')
        print("🟢 (1/5) Successfully opened Deepgram streaming connection")

        async def sender(ws):
            print(
                f'🟢 (2/5) Ready to stream {method} audio to Deepgram{". Speak into your microphone to transcribe."}'
            )

            if method == "mic":
                try:
                    while True:
                        mic_data = await audio_queue.get()
                        all_mic_data.append(mic_data)
                        await ws.send(mic_data)

                except websockets.exceptions.ConnectionClosedOK:
                    await ws.send(json.dumps({"type": "CloseStream"}))
                    print(
                        "🟢 (5/5) Successfully closed Deepgram connection, waiting for final transcripts if necessary"
                    )

                except Exception as e:
                    print(f"Error while sending: {str(e)}")
                    raise

            else:
                raise Exception("Did you mispell mic?")

            return

        async def receiver(ws):
            """Print out the messages received from the server."""
            first_message = True
            first_transcript = True
            transcript = ""

            async for msg in ws:
                res = json.loads(msg)
                if first_message:
                    print(
                        "🟢 (3/5) Successfully receiving Deepgram messages, waiting for finalized transcription..."
                    )
                    first_message = False
                try:
                    # handle local server messages
                    if res.get("msg"):
                        print(res["msg"])
                    if res.get("is_final"):
                        transcript = (
                            res.get("channel", {})
                            .get("alternatives", [{}])[0]
                            .get("transcript", "")
                        )
                        if kwargs["timestamps"]:
                            words = res.get("channel", {}).get("alternatives", [{}])[0].get("words", [])
                            start = words[0]["start"] if words else None
                            end = words[-1]["end"] if words else None
                            transcript += " [{} - {}]".format(start, end) if (start and end) else ""
                        if transcript != "":
                            if first_transcript:
                                print("🟢 (4/5) Began receiving transcription")
                                # if using webvtt, print out header
                                if format == "vtt":
                                    print("WEBVTT\n")
                                first_transcript = False
                            print(transcript)
                            all_transcripts.append(transcript)
                        
                        if method == "mic" and any(word in transcript.lower() for word in STOP_WORDS):
                             await ws.send(json.dumps({"type": "CloseStream"}))
                             print("🟢 (5/5) Successfully closed Deepgram connection, waiting for final transcripts if necessary")

                        # # if using the microphone, close stream if user says "goodbye"
                        # if method == "mic" and "goodbye" in transcript.lower():
                        #     await ws.send(json.dumps({"type": "CloseStream"}))
                        #     print(
                        #         "🟢 (5/5) Successfully closed Deepgram connection, waiting for final transcripts if necessary"
                        #     )

                    # handle end of stream
                    if res.get("created"):
                        data_dir = 'output/buffer/transcripts'
                        transcript_file_path = os.path.abspath(
                            os.path.join(
                                data_dir,
                                f'{kwargs["slide"]}.txt'
                            )
                        )
                        
                        with open(transcript_file_path, "w") as f:
                            f.write("".join(add_whitespace(all_transcripts)))
                        print(f"🟢 Transcript saved to {transcript_file_path}")
                        print(
                            f'🟢 Request finished with a duration of {res["duration"]} seconds. Exiting!'
                        )
                except KeyError:
                    print(f":🔴 ERROR Received unexpected API response! {msg}")

        # Set up microphone if streaming from mic
        async def microphone():
            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=mic_callback,
            )

            stream.start_stream()

            global SAMPLE_SIZE
            SAMPLE_SIZE = audio.get_sample_size(FORMAT)

            while stream.is_active():
                await asyncio.sleep(0.1)

            stream.stop_stream()
            stream.close()

        functions = [
            asyncio.ensure_future(sender(ws)),
            asyncio.ensure_future(receiver(ws)),
        ]

        if method == "mic":
            functions.append(asyncio.ensure_future(microphone()))

        await asyncio.gather(*functions)

def generate_summary_file(topic, PATH='data/1234.json'):
    if not os.path.exists(PATH):
        empty_dict = {
            "presentation_ID": 1234,
            "topic": f"{topic}",
            "slides": []
            }
        with open(PATH, 'w') as json_file:
            json.dump(empty_dict, json_file, indent=3)

def main():
    args = parse_args()
    input = args.input
    format = args.format.lower()
    host = args.host
    topic = args.topic
    API_KEY = os.environ['DEEPGRAM_API_KEY']

    generate_summary_file(topic)

    try:
        if input.lower().startswith("mic"):
            asyncio.run(run(API_KEY, "mic", format, model=args.model, tier=args.tier, host=host, timestamps=args.timestamps, slide=args.slide))
        else:
            raise argparse.ArgumentTypeError(
                f'🔴 {input} is an invalid input. Please enter the path to a WAV file, a valid stream URL, or "mic" to stream from your microphone.'
            )

    except websockets.exceptions.InvalidStatusCode as e:
        print(f'🔴 ERROR: Could not connect to Deepgram! {e.headers.get("dg-error")}')
        print(
            f'🔴 Please contact Deepgram Support (developers@deepgram.com) with request ID {e.headers.get("dg-request-id")}'
        )
        return
    except websockets.exceptions.ConnectionClosedError as e:
        error_description = f"Unknown websocket error."
        print(
            f"🔴 ERROR: Deepgram connection unexpectedly closed with code {e.code} and payload {e.reason}"
        )

        if e.reason == "DATA-0000":
            error_description = "The payload cannot be decoded as audio. It is either not audio data or is a codec unsupported by Deepgram."
        elif e.reason == "NET-0000":
            error_description = "The service has not transmitted a Text frame to the client within the timeout window. This may indicate an issue internally in Deepgram's systems or could be due to Deepgram not receiving enough audio data to transcribe a frame."
        elif e.reason == "NET-0001":
            error_description = "The service has not received a Binary frame from the client within the timeout window. This may indicate an internal issue in Deepgram's systems, the client's systems, or the network connecting them."

        print(f"🔴 {error_description}")
        # TODO: update with link to streaming troubleshooting page once available
        # print(f'🔴 Refer to our troubleshooting suggestions: ')
        print(
            f"🔴 Please contact Deepgram Support (developers@deepgram.com) with the request ID listed above."
        )
        return

    except websockets.exceptions.ConnectionClosedOK:
        return

    except Exception as e:
        print(f"🔴 ERROR: Something went wrong! {e}")
        return


if __name__ == "__main__":
    sys.exit(main() or 0)
