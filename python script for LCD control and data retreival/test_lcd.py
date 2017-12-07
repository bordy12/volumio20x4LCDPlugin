from lcd_display import lcd

lcd_positie=[1,1,3,2,4] #Zet alle posities in een array. Nu kan het script ten alle tijden de goede positie versturen d.m.v. lcd_positie[x].
my_lcd = lcd()
my_lcd.display_string("Boomer", lcd_positie[1])
#my_lcd.display_string("", lcd_positie[2])
#my_lcd.display_string("", lcd_positie[3])
#my_lcd.display_string("", lcd_positie[4])

