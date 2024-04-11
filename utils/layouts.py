
class CustomLayouts:
    def __init__(self):
        self.dimensions = {'title' : {'left': 0.5, 'top': 0.3, 'width': 9, 'height': 1.25}}
    
    def get_layout_dimensions(self, layout_id):
        match layout_id:

            ## Only Title
            case 0:
                self.dimensions['title'] = {'left': 0.5, 'top': 2, 'width': 9, 'height': 1.25}
            ## Title and One Big Element
            case 1:
                self.dimensions['body'] = [{'type': 0,  'left': 0.5, 'top': 2, 'width': 9, 'height': 5}] 
            ## Title and two elements in two-column format
            case 2:
                self.dimensions['body'] = [{'type': 1, 'left': 0.5, 'top': 2, 'width': 4.5, 'height': 4}, {'type': 1, 'left': 5, 'top': 2, 'width': 4.5, 'height': 4}]
            ## Title and two elements in two-row format
            case 3:
                self.dimensions['body'] = [{'type' : 2, 'left': 0.5, 'top': 2, 'width': 9, 'height': 2.5}, {'type' : 2, 'left': 0.5, 'top': 4.5, 'width': 9, 'height': 2.5}] 
            case 4:
                self.dimensions['body'] = [{'type' : 3, 'left': 0.5, 'top': 2, 'width': 3, 'height': 4}, {'type' : 3, 'left': 3.5, 'top': 2, 'width': 3, 'height': 4}, {'type' : 3, 'left': 6.5, 'top': 2, 'width': 3, 'height': 4}]
            case 5: 
                self.dimensions['body'] = [{'type': 1, 'left': 0.5, 'top': 2, 'width': 4.5, 'height': 4}, {'type': 4, 'left': 5, 'top': 2, 'width': 4.5, 'height': 2}, {'type': 4, 'left': 5, 'top': 4, 'width': 4.5, 'height': 2}]
            case 6:
                self.dimensions['body'] = [{'type': 4, 'left': 0.5, 'top': 2, 'width': 4.5, 'height': 2}, {'type': 4, 'left': 0.5, 'top': 4, 'width': 4.5, 'height': 2}, {'type': 1, 'left': 5, 'top': 2, 'width': 4.5, 'height': 4}]
            case 7:
                self.dimensions['body'] = [{'type' : 4, 'left': 0.5, 'top': 2, 'width': 4.5, 'height': 2}, {'type' : 4, 'left': 5, 'top': 2, 'width': 4.5, 'height': 2}, {'type' : 2, 'left': 0.5, 'top': 4.5, 'width': 9, 'height': 2.5}]
            case 8:
                self.dimensions['body'] = [{'type' : 4, 'left': 0.5, 'top': 4.5, 'width': 4.5, 'height': 2}, {'type' : 4, 'left': 5, 'top': 4.5, 'width': 4.5, 'height': 2}, {'type' : 2, 'left': 0.5, 'top': 2, 'width': 9, 'height': 2.5}] 


                
            # Layout Error Default
            case _:
                raise Exception("Layout Definition Error : No layout defined")

        return self.dimensions 
