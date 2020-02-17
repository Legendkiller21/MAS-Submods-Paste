# Original Paste code and Sub-Selections v2 by LegendKiller21
# Copy, Cut, Select All, and Original Markers for Sub-Selections and Sub-Selections v2 optimizations by LordBaaa

init 1 python:
    config.keymap['input_paste'] = ['ctrl_K_v']

    #Additional Edit Shortcuts
    config.keymap['input_copy'] = ['ctrl_K_c']
    config.keymap['input_cut'] = ['ctrl_K_x']
    config.keymap['input_select_all'] = ['ctrl_K_a']

    # Allows you to use CRTL + arrow keys to move the markers
    # NOTE: the windows shortcut is shift + arrow keys but we can't use shift shortcuts in console
    config.keymap['input_move_start_marker_pos'] = ['ctrl_K_LEFT', 'ctrl_repeat_K_LEFT']
    config.keymap['input_move_end_marker_pos'] = ['ctrl_K_RIGHT', 'ctrl_repeat_K_RIGHT']

init 999 python:

    #Sets new Input class variables
    setattr(renpy.display.behavior.Input, 'start_marker_pos', 0)
    setattr(renpy.display.behavior.Input, 'end_marker_pos', 0)
    setattr(renpy.display.behavior.Input, 'start_marker_is_set', False)
    setattr(renpy.display.behavior.Input, 'end_marker_is_set', False)
    setattr(renpy.display.behavior.Input, 'start_marker_text', "\u231C")
    setattr(renpy.display.behavior.Input, 'end_marker_text', "\u231F")

    #Input Class new Functions
    def class_Input_remove_marker_text(self, content):
        """
        Removes selection Marker text
        IN:
        content: 
        type(str/unicode)
        
        OUT:
        content:
        string that has start and end marker text removed
        """
        return content.replace(self.start_marker_text,"").replace(self.end_marker_text,"")


    def class_Input_reset_marker_values(self):
        """ Resets all marker values """
        self.start_marker_pos = 0
        self.end_marker_pos = 0
        self.start_marker_is_set = False
        self.end_marker_is_set = False

    def class_Input_reset_screen_markers(self):
        """
        Resets Marker Values and Removes Markers from Screen
        """

        #Removes markers if function didn't succeed
        content_removed_markers = self.remove_marker_text(self.content)
        self.reset_marker_values()

        #Update Display
        self.update_text(content_removed_markers, self.editable, check_size=True)
    #Input Class new Functions
    
    def class_Input_process_set_marker_pos(self, text_mode, pos_mode):
        """
        Adjusts marker text and marker set postions
 
        IN:
        string: string
        String to have operations done on it
        
        text_mode: int
        Changes what marker text and actual postion is is affected 
        
        pos_mode: int
        Gets the value of postion to be affected and what operation is done to it.
        
        OUT:
        content: string
        processed content 
        """
        marker_text = [self.start_marker_text, self.end_marker_text]
        marker_postion = [self.start_marker_pos, self.end_marker_pos]
        marker_offset = [-1, 1]
        
        content = list(self.content.replace(marker_text[text_mode],""))
        content.insert(marker_postion[text_mode] + marker_offset[pos_mode], marker_text[text_mode])
        
        if text_mode == 0:
            self.start_marker_pos += marker_offset[pos_mode]
         
        elif text_mode == 1:
            self.end_marker_pos += marker_offset[pos_mode]

        return content

     
    def class_Input_marker_set_else_code(self, mode):
        """
        IN:
        mode: int
        picks start and end int_lits
        """
        mode = int(mode)
        start_int_list = [-1, 0]
        end_int_list = [1, 2]
        if self.end_marker_is_set and self.caret_pos > self.end_marker_pos:
            self.caret_pos -=2
        elif self.end_marker_is_set and self.start_marker_pos < self.caret_pos < self.end_marker_pos:
            self.caret_pos -=1
        content = list(self.remove_marker_text(self.content))

        self.start_marker_pos = self.caret_pos + start_int_list[mode]
        content.insert(self.caret_pos + start_int_list[mode], self.start_marker_text)
        self.start_marker_is_set = True    
            
        self.end_marker_pos = self.caret_pos + end_int_list[mode]
        content.insert(self.caret_pos + end_int_list[mode], self.end_marker_text)
        self.end_marker_is_set = True

        return content
        
    def class_Input_copy_function(self, content, cut = False):
        """
        Copies/Cuts content of the console input
        
        content: string
        String to be processed
        cut: bool
        Sets if code will just cut or just copy
        """
        if self.start_marker_is_set and self.end_marker_is_set:
                    
            #Makes sure Start Marker is before End Marker
            if self.end_marker_pos > self.start_marker_pos:

                #Removes Markers and copies to clipboard
                content_removed_markers = self.remove_marker_text(self.content)
                copy_content = content_removed_markers[self.start_marker_pos : self.end_marker_pos-1]
                pygame.scrap.put(pygame.SCRAP_TEXT,copy_content)
                if cut: 
                    #Removes cut content from string that will be sent to the screen
                    cut_content = "{0}{1}{2}".format(content_removed_markers[0:self.start_marker_pos], "", content_removed_markers[self.end_marker_pos-1:len(content_removed_markers)])

                    #Update Display
                    self.caret_pos = self.start_marker_pos
                    self.update_text(cut_content, self.editable, check_size=True)

                else:
                    #Update Display
                    self.update_text(content_removed_markers, self.editable, check_size=True)
                    #Reset
                    self.reset_marker_values()
        else:
            self.reset_screen_markers()
            
        #Finish Updating Display
        renpy.display.render.redraw(self, 0)
        raise renpy.display.core.IgnoreEvent()

    #Adds fuctions to Input Class
    setattr(renpy.display.behavior.Input, 'remove_marker_text', class_Input_remove_marker_text)
    setattr(renpy.display.behavior.Input, 'reset_marker_values', class_Input_reset_marker_values)
    setattr(renpy.display.behavior.Input, 'reset_screen_markers', class_Input_reset_screen_markers)
    setattr(renpy.display.behavior.Input, 'process_set_marker_pos', class_Input_process_set_marker_pos)
    setattr(renpy.display.behavior.Input, 'marker_set_else_code', class_Input_marker_set_else_code)
    setattr(renpy.display.behavior.Input, 'copy_function', class_Input_copy_function)
    
    map_event = renpy.display.behavior.map_event

    def event_ov(self, ev, x, y, st):
        self.old_caret_pos = self.caret_pos

        if not self.editable:
            return None

        l = len(self.content)

        raw_text = None

        if map_event(ev, "input_backspace"):
            if self.content:
                if (
                    self.start_marker_is_set
                    and self.end_marker_is_set
                    and self.start_marker_pos == 0
                    and self.end_marker_pos == l
                ):
                    content = self.content[0:0]
                    self.caret_pos = self.start_marker_pos
                    self.reset_marker_values()

                    #Updates Display
                    self.update_text(content, self.editable)

                elif self.caret_pos > 0:
                    content = self.content[0:self.caret_pos-1] + self.content[self.caret_pos:l]
                    self.caret_pos -= 1
                    self.update_text(content, self.editable)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_enter"):

            content = self.content

            if self.edit_text:
                content = content[0:self.caret_pos] + self.edit_text + self.content[self.caret_pos:]

            if self.value:
                return self.value.enter()

            if not self.changed:
                return content

        elif map_event(ev, "input_left"):
            if self.caret_pos > 0:
                self.caret_pos -= 1
                self.update_text(self.content, self.editable)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_right"):
            if self.caret_pos < l:
                self.caret_pos += 1
                self.update_text(self.content, self.editable)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_delete"):
            if (
                self.start_marker_is_set
                and self.end_marker_is_set
                and self.start_marker_pos == 0
                and self.end_marker_pos == l
            ):
                content = self.content[0:0]
                self.caret_pos = self.start_marker_pos
                self.reset_marker_values()

                #Updates Display
                self.update_text(content, self.editable)

            elif self.caret_pos < l:
                content = self.content[0:self.caret_pos] + self.content[self.caret_pos+1:l]
                self.update_text(content, self.editable)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()
        

        elif map_event(ev, "input_paste"):
            content = self.content[0:self.caret_pos] + pygame.scrap.get(pygame.SCRAP_TEXT) + self.content[self.caret_pos:l]
            if self.start_marker_is_set and self.end_marker_is_set:
                if self.caret_pos < self.start_marker_pos:
                    self.start_marker_pos += len(pygame.scrap.get(pygame.SCRAP_TEXT))
                    self.end_marker_pos += len(pygame.scrap.get(pygame.SCRAP_TEXT))-1
                elif self.start_marker_pos < self.caret_pos < self.end_marker_pos:
                    self.end_marker_pos += len(pygame.scrap.get(pygame.SCRAP_TEXT))-1
                else:
                    self.end_marker_pos -= 1
            self.caret_pos += len(pygame.scrap.get(pygame.SCRAP_TEXT))
            self.update_text(content, self.editable, check_size=True)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_copy"):
            self.copy_function(self.content)
            
        elif map_event(ev, "input_cut"):
            self.copy_function(self.content, True)


        elif map_event(ev, "input_move_start_marker_pos"):
            #shift left
            if self.content and self.caret_pos > 0:
                
                #Checks that the start and end Markers have been set and checks if the current caret_pos is either the start/end marker postion
                if (
                    self.start_marker_is_set and self.end_marker_is_set
                    and (self.caret_pos == self.end_marker_pos
                        or self.caret_pos == self.start_marker_pos
                    )
                ):
                    #If caret is at that start postion
                    if self.caret_pos == self.start_marker_pos:
                        content = self.process_set_marker_pos(0,0)
                        
                    elif self.caret_pos == self.end_marker_pos:
                        content = self.process_set_marker_pos(1,0)
                        
                    if self.start_marker_pos == self.end_marker_pos-1:
                        content = list(self.remove_marker_text(self.content))
                        self.reset_marker_values()
                        self.caret_pos -=1

                
                else:
                    content = self.marker_set_else_code(0)
                self.caret_pos -= 1

                content = "".join(content)

                #Update Screen
                self.update_text(content, self.editable, check_size=True)
            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()
          
        elif map_event(ev, "input_move_end_marker_pos"):
            #shift right
            if self.content and self.caret_pos < l:

                if (
                    self.start_marker_is_set and self.end_marker_is_set
                    and (self.caret_pos == self.end_marker_pos
                        or self.caret_pos == self.start_marker_pos
                    )
                ):
                    if self.caret_pos == self.start_marker_pos:
                        content = self.process_set_marker_pos(0,1)

                    elif self.caret_pos == self.end_marker_pos:
                        content = self.process_set_marker_pos(1,1)

                    if self.start_marker_pos == self.end_marker_pos-1:
                        content = list(self.remove_marker_text(self.content))
                        self.reset_marker_values()

                    self.caret_pos += 1

                else:
                    content = self.marker_set_else_code(1)  
                    self.caret_pos += 2
                content = "".join(content)

                #Update Screen
                self.update_text(content, self.editable, check_size=True)
            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_select_all"):
            if self.content:
                #Set Vars
                self.start_marker_pos = 0
                self.end_marker_pos = l
                self.caret_pos += 1
                content_removed_markers = self.remove_marker_text(self.content)
                content = "{0}{1}{2}".format(self.start_marker_text, content_removed_markers , self.end_marker_text)

                #We know all else has been successful so we set this to True for Copy Code
                self.start_marker_is_set = True
                self.end_marker_is_set = True

                #Update Screen
                self.update_text(content, self.editable, check_size=True)
                #Re-adjust the end pos to its true position so backspace and delete can erase everything
                self.end_marker_pos = len(self.content)
                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()
            
        elif map_event(ev, "input_home"):
            self.caret_pos = 0
            self.update_text(self.content, self.editable)
            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_end"):
            
            self.caret_pos = l
            self.update_text(self.content, self.editable)
            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif ev.type == pygame.TEXTEDITING:
            self.update_text(self.content, self.editable, check_size=True)

            raise renpy.display.core.IgnoreEvent()

        elif ev.type == pygame.TEXTINPUT:
            self.edit_text = ""
            raw_text = ev.text

        elif ev.type == pygame.KEYDOWN:
            if ev.unicode and ord(ev.unicode[0]) >= 32:
                raw_text = ev.unicode
            elif renpy.display.interface.text_event_in_queue():
                raw_text = ''

        if raw_text is not None:

            text = ""

            for c in raw_text:

                if self.allow and c not in self.allow:
                    continue
                if self.exclude and c in self.exclude:
                    continue

                text += c

            if self.length:
                remaining = self.length - len(self.content)
                text = text[:remaining]

            if text:

                content = self.content[0:self.caret_pos] + text + self.content[self.caret_pos:l]
                self.caret_pos += len(text)

                self.update_text(content, self.editable, check_size=True)

            raise renpy.display.core.IgnoreEvent()

    setattr(renpy.display.behavior.Input, 'event', event_ov)
