

class DigitalDigits():
    __framebuffer = None
    __x = 0
    __y = 0
    __width = 0
    __height = 0
    __digit_width = 0
    __digit_height = 0
    __space_between_digits = 0
    __segment_thickness = 4
    __segment_space = 0
    __segment_height = 0
    __segment_width = 0
    __value = 0.00
    __point_already_past = False
    __white = 1
    __black = 0


    def __init__(self,
        framebuffer,
        x,
        y,
        width,
        height,
        space_between_digits,
        segment_space,
        segment_thickness
        ):
        """Initialisiert ein DigitalDigits Objekt.
        Die Koordinaten(x,y) geben die obere linke Ecke an.
        Die Breite und Höhe gibt den Rahmen vor in dem die Ziffern angezeigt werden.
        Es werden ein paar Berechnungen gemacht, um z.B. die Höhe eines Segments zu bestimmen."""
        self.__framebuffer = framebuffer
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        #self.__digit_width = int((width -((4-1) * (space_between_digits)))/ 4)
        self.__digit_height = height
        self.__space_between_digits = space_between_digits
        self.__segment_space = segment_space
        self.__segment_thickness = segment_thickness

        self.__framebuffer.fill(self.__white)

    
    def __calc(self):
        value_str = str(self.__value)
        value_length = len(value_str)
        point_width = 0

        if "." in value_str:
            value_length -= 1
            point_width = self.__segment_thickness + self.__space_between_digits

        # Digit Weite
        self.__digit_width = int(self.__width / len(value_str)) # Komplette Breite durch die Anzahl der Digits
        self.__digit_width -= self.__space_between_digits # Zwischenraum abziehen
        self.__digit_width += int(self.__space_between_digits / len(value_str)) # Der letzte Zwischenraum wird wieder gutgeschrieben
        
        if "." in value_str:
            self.__digit_width += int((self.__digit_width - self.__segment_thickness) / value_length)# Da der Punkt kleiner ist wird die Differenz dazu addiert
        

        # Segment Höhe
        self.__segment_height = int((self.__digit_height / 2) - int(self.__segment_thickness / 2)) - 1

        # Segment Weite
        self.__segment_width = self.__digit_width - self.__segment_thickness - 1

        # Länge der Spitze eines Segments
        self.__tip_size = int(self.__segment_thickness / 2)


    def set_value(self, value):
        self.__value = value
        self.__calc()

        value_str = str(self.__value)
        self.__point_already_past = False
        for i in range(0, len(value_str)):
            if value_str[i] == ".":
                self.__draw_point(i)
                self.__point_already_past = True
            else:
                self.__draw_digit(i, int(value_str[i]))


    def invert(self):
        self.__white, self.__black = self.__black, self.__white
        self.__framebuffer.fill(self.__white)
    

    def __draw_point(self, pos):
        offset_x = self.__x + ((pos * self.__digit_width) + (pos * self.__space_between_digits))
        offset_y = self.__y + self.__digit_height - self.__segment_thickness
        for i in range(0, self.__tip_size):
            self.__framebuffer.vline(
                offset_x + self.__tip_size - i,
                offset_y + i,
                self.__segment_thickness-(i * 2),
                self.__black)
        for i in range(0, self.__tip_size):
            self.__framebuffer.vline(
                offset_x + (self.__tip_size) + i,
                offset_y + i,
                self.__segment_thickness-(i * 2),
                self.__black)

    
    def __draw_digit(self, pos, digit):
        """"""
        if digit == 0:
            self.__draw_segments(pos, [0, 1, 2, 4, 5, 6])
        if digit == 1:
            self.__draw_segments(pos, [2, 5])
        if digit == 2:
            self.__draw_segments(pos, [0, 2, 3, 4, 6])
        if digit == 3:
            self.__draw_segments(pos, [0, 2, 3, 5, 6])
        if digit == 4:
            self.__draw_segments(pos, [1, 2, 3, 5])
        if digit == 5:
            self.__draw_segments(pos, [0, 1, 3, 5, 6])
        if digit == 6:
            self.__draw_segments(pos, [0, 1, 3, 4, 5, 6])
        if digit == 7:
            self.__draw_segments(pos, [0, 2, 5])
        if digit == 8:
            self.__draw_segments(pos, [0, 1, 2, 3, 4, 5, 6])
        if digit == 9:
            self.__draw_segments(pos, [0, 1, 2, 3, 5, 6])
            


    def __draw_segments(self, pos, segment_numbers):
        """Bestimmt welche Segmente gezeichnet werden sollen.
          ###0###
        #         #
        1         2
        #         #
          ###3###
        #         #
        4         5
        #         #
          ###6###"""

        offset_x = (pos * self.__digit_width) + (pos * self.__space_between_digits)

        # negative space after point is drawn
        if self.__point_already_past:
            offset_x -= self.__digit_width - self.__segment_thickness

        if 0 in segment_numbers:
            self.__draw_h_segment(self.__x + offset_x + int(self.__segment_thickness / 2) , self.__y)
        if 1 in segment_numbers:
            self.__draw_v_segment(self.__x + offset_x, self.__y + int(self.__segment_thickness / 2))
        if 2 in segment_numbers:
            self.__draw_v_segment(
                    self.__x + offset_x + self.__digit_width - self.__segment_thickness,
                    self.__y + int(self.__segment_thickness / 2))
        if 3 in segment_numbers:
            self.__draw_h_segment(self.__x + offset_x + int(self.__segment_thickness / 2), self.__y + self.__segment_height + 1)
        if 4 in segment_numbers:
            self.__draw_v_segment(self.__x + offset_x, self.__y + self.__segment_height + int(self.__segment_thickness / 2) + 1)
        if 5 in segment_numbers:
            self.__draw_v_segment(
                    self.__x + offset_x + self.__digit_width - self.__segment_thickness,
                    self.__y + self.__segment_height + int(self.__segment_thickness / 2) + 1)
        if 6 in segment_numbers:
            self.__draw_h_segment(self.__x + offset_x + int(self.__segment_thickness / 2), self.__digit_height - self.__segment_thickness)


    def __draw_v_segment(self, offset_x, offset_y):
        self.__framebuffer.fill_rect(
            offset_x,
            offset_y + self.__tip_size,
            self.__segment_thickness,
            self.__segment_height - (2 * self.__tip_size),
            self.__black)
        for i in range(0, self.__tip_size):
            self.__framebuffer.hline(
                offset_x + i,
                offset_y + self.__tip_size - i,
                self.__segment_thickness-(i * 2),
                self.__black)
        for i in range(0, self.__tip_size):
            self.__framebuffer.hline(
                offset_x + i,
                offset_y + self.__segment_height - self.__tip_size + i,
                self.__segment_thickness-(i * 2),
                self.__black)
        
    def __draw_h_segment(self, offset_x, offset_y):
        self.__framebuffer.fill_rect(
            offset_x + self.__tip_size,
            offset_y,
            self.__segment_width - (self.__tip_size * 2),
            self.__segment_thickness,
            self.__black)
        for i in range(0, self.__tip_size):
            self.__framebuffer.vline(
                offset_x + self.__tip_size - i,
                offset_y + i,
                self.__segment_thickness-(i * 2),
                self.__black)
        for i in range(0, self.__tip_size):
            self.__framebuffer.vline(
                offset_x + self.__segment_width - (self.__tip_size) + i,
                offset_y + i,
                self.__segment_thickness-(i * 2),
                self.__black)

    