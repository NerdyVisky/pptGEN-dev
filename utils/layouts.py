MUL_FAC = 1
class CustomLayouts:
    def __init__(self):
        self.dimensions = {'title' : {'type': 1, 'left': 0.5, 'top': 0.3, 'width': 9*MUL_FAC, 'height': 1.25},
                           'footer': [{'type' : 1, 'left': 0.5, 'top': 7, 'width': 3*MUL_FAC, 'height': 0.5}, {'type' : 2, 'left': 3.5*MUL_FAC, 'top': 7, 'width': 3*MUL_FAC, 'height': 0.5}, {'type' : 3, 'left': 6.5*MUL_FAC, 'top': 7, 'width': 3*MUL_FAC, 'height': 0.5}]}
    
    def get_layout_dimensions(self, layout_id):
        match layout_id:

            ## Only Title
            case 0:
                self.dimensions['title'] = {'type': 0, 'left': 0.5, 'top': 2, 'width': 9*MUL_FAC, 'height': 1.25}
            ## Title and One Big Element
            case 1:
                self.dimensions['body'] = [{'type': 0,  'left': 0.5, 'top': 2, 'width': 9*MUL_FAC, 'height': 5}] 
            ## Title and two elements in two-column format
            case 2:
                self.dimensions['body'] = [{'type': 1, 'left': 0.5, 'top': 2, 'width': 4.5*MUL_FAC, 'height': 5}, {'type': 1, 'left': 5*MUL_FAC, 'top': 2, 'width': 4.5*MUL_FAC, 'height': 5}]
            ## Title and two elements in two-row format
            case 3:
                self.dimensions['body'] = [{'type' : 2, 'left': 0.5, 'top': 2, 'width': 9*MUL_FAC, 'height': 2.5}, {'type' : 2, 'left': 0.5, 'top': 4.5, 'width': 9*MUL_FAC, 'height': 2.5}] 
            case 4:
                self.dimensions['body'] = [{'type' : 3, 'left': 0.5, 'top': 2, 'width': 3*MUL_FAC, 'height': 5}, {'type' : 3, 'left': 3.5*MUL_FAC, 'top': 2, 'width': 3*MUL_FAC, 'height': 5}, {'type' : 3, 'left': 6.5*MUL_FAC, 'top': 2, 'width': 3*MUL_FAC, 'height': 5}]
            case 5: 
                self.dimensions['body'] = [{'type': 1, 'left': 0.5, 'top': 2, 'width': 4.5*MUL_FAC, 'height': 5}, {'type': 4, 'left': 5*MUL_FAC, 'top': 2, 'width': 4.5*MUL_FAC, 'height': 2.5}, {'type': 4, 'left': 5*MUL_FAC, 'top': 4.5, 'width': 4.5*MUL_FAC, 'height': 2.5}]
            case 6:
                self.dimensions['body'] = [{'type': 4, 'left': 0.5, 'top': 2, 'width': 4.5*MUL_FAC, 'height': 2.5}, {'type': 4, 'left': 0.5, 'top': 4.5, 'width': 4.5*MUL_FAC, 'height': 2.5}, {'type': 1, 'left': 5*MUL_FAC, 'top': 2, 'width': 4.5*MUL_FAC, 'height': 5}]
            case 7:
                self.dimensions['body'] = [{'type' : 4, 'left': 0.5, 'top': 2, 'width': 4.5*MUL_FAC, 'height': 2.5}, {'type' : 4, 'left': 5*MUL_FAC, 'top': 2, 'width': 4.5*MUL_FAC, 'height': 2.5}, {'type' : 2, 'left': 0.5, 'top': 4.5, 'width': 9*MUL_FAC, 'height': 2.5}]
            case 8:
                self.dimensions['body'] = [{'type' : 4, 'left': 0.5, 'top': 4.5, 'width': 4.5*MUL_FAC, 'height': 2.5}, {'type' : 4, 'left': 5*MUL_FAC, 'top': 4.5, 'width': 4.5*MUL_FAC, 'height': 2.5}, {'type' : 2, 'left': 0.5, 'top': 2, 'width': 9*MUL_FAC, 'height': 2.5}] 
            # Layout Error Default
            case _:
                raise Exception("Layout Definition Error : No layout defined")
        return self.dimensions 
