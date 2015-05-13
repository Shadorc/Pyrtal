class Rect():

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.centerX = self.x + self.width/2
        self.centerY = self.y + self.height/2

    def intersects(self, rect):
        if(abs(self.centerX - rect.centerX) < (self.width + rect.width )/2 and abs(self.centerY - rect.centerY) < (self.height+rect.height)/2):
            return True
        else:
            return False

    def perspective(self, rect):
        if(self.intersects(rect) and (rect.y-20 + rect.height < self.y + self.height < rect.y+20 + rect.height)):
            return True
        else:
            return False

    """          width/2
              <--------->
    +-------------------+
    |                   |
    |       (x, y)      |
    |         +         |
    |              +----|---------------+
    |              |    |               |     |x-x1| < (width+width1)/2 and |y-y1| < (height+height1)/2
    +-------------------+    (x1, y1)   |
                   |         +          |
                   |                    |
                   |                    |
                   +--------------------+
                   <--------->                    
                    width1/2

    """
