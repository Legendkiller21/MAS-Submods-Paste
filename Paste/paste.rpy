# Original Paste code by LegendKiller21
# Copy, Cut, Select All, and Markers for Sub-Selections by LordBaaa

init 1 python:
    config.keymap['input_paste'] = ['ctrl_K_v']
   
    #Additional Edit Shortcuts
    config.keymap['input_copy'] = ['ctrl_K_c']
    config.keymap['input_cut'] = ['ctrl_K_x']
    config.keymap['input_select_all'] = ['ctrl_K_a']
    
    # Allows you to use CRTL + 1,2 or q,w if you like it to a little closer
    config.keymap['input_set_start_marker_pos'] = ['ctrl_K_1', 'ctrl_K_q']
    config.keymap['input_set_end_marker_pos'] = ['ctrl_K_2', 'ctrl_K_w']
    
init 999 python:

    #Sets new Input class variables
    setattr(renpy.display.behavior.Input, 'start_marker_pos', 0)
    setattr(renpy.display.behavior.Input, 'end_marker_pos', 0)
    setattr(renpy.display.behavior.Input, 'start_marker_is_set', False)
    setattr(renpy.display.behavior.Input, 'end_marker_is_set', False)
    setattr(renpy.display.behavior.Input, 'start_marker_text', "@[")
    setattr(renpy.display.behavior.Input, 'end_marker_text', "]@")
    
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
    
    #Adds fuctions to Input Class
    setattr(renpy.display.behavior.Input, 'remove_marker_text', class_Input_remove_marker_text)
    setattr(renpy.display.behavior.Input, 'reset_marker_values', class_Input_reset_marker_values)
    setattr(renpy.display.behavior.Input, 'reset_screen_markers', class_Input_reset_screen_markers)

    map_event = renpy.display.behavior.map_event
    
    def event_ov(self, ev, x, y, st):   
        self.old_caret_pos = self.caret_pos

        if not self.editable:
            return None

        l = len(self.content)

        raw_text = None

        if map_event(ev, "input_backspace"):

            if self.content and self.caret_pos > 0:
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
            if self.caret_pos < l:
                content = self.content[0:self.caret_pos] + self.content[self.caret_pos+1:l]
                self.update_text(content, self.editable)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()
        

        elif map_event(ev, "input_paste"):
            content = self.content[0:self.caret_pos] + pygame.scrap.get(pygame.SCRAP_TEXT) + self.content[self.caret_pos:l]
            self.caret_pos += len(pygame.scrap.get(pygame.SCRAP_TEXT))
            self.update_text(content, self.editable, check_size=True)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_copy"):
        
            #Checks if one of the Markers are set
            if self.start_marker_is_set or self.end_marker_is_set == True:
            
                #Makes sure both Markers are set
                if self.start_marker_is_set and self.end_marker_is_set == True:
            
                    #Makes sure Start Marker is before End Marker
                    if self.end_marker_pos > self.start_marker_pos:
            
                        #Removes Markers and copies to clipboard
                        content_removed_markers = self.remove_marker_text(self.content)
                        copy_content = content_removed_markers[self.start_marker_pos : self.end_marker_pos]
                        pygame.scrap.put(pygame.SCRAP_TEXT,copy_content)
                 
                        #Update Display
                        self.update_text(content_removed_markers, self.editable, check_size=True)

                        #Reset
                        self.reset_marker_values()
                    #If Start Marker is after End Marker Reset Screen
                    else:
                        self.reset_screen_markers()
                else:
                    self.reset_screen_markers()
                    
              
            #Finish Updating Display
            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()
            
        elif map_event(ev, "input_cut"):
        
            #Checks if one of the Markers are set
            if self.start_marker_is_set or self.end_marker_is_set == True:
            
                #Makes sure both Markers are set
                if self.start_marker_is_set and self.end_marker_is_set == True:
            
                    #Makes sure Start Marker is before End Marker
                    if self.end_marker_pos > self.start_marker_pos:
            
                        #Removes Markers and copies to clipboard
                        content_removed_markers = self.remove_marker_text(self.content)
                        cut_content = "{0}{1}{2}".format(content_removed_markers[0:self.start_marker_pos], "", content_removed_markers[self.end_marker_pos:l])
                        copy_content = content_removed_markers[self.start_marker_pos : self.end_marker_pos]
                        pygame.scrap.put(pygame.SCRAP_TEXT, copy_content)
              
                        #Reset
                        self.caret_pos = self.start_marker_pos
                        self.reset_marker_values()

                        #Updates Display
                        self.update_text(cut_content, self.editable)
                    #If Start Marker is after End Marker Reset Screen
                    else:
                        self.reset_screen_markers()
                else:
                    self.reset_screen_markers()
                    
              
            #Finish Updating Display
            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()
               

            #Finish Updating Display
            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()
            
        elif map_event(ev, "input_set_start_marker_pos"):
            #Set Vars
            self.start_marker_pos = self.caret_pos
             
            #Divide and recombine content with Start Marker
            content = list(self.content.replace(self.start_marker_text,""))
            content.insert(self.caret_pos, self.start_marker_text) 
            content = "".join(content)
           
            #We know all else has been successful so we set this to True for Copy Code
            self.start_marker_is_set = True
           
            #Update Screen
            self.update_text(content, self.editable, check_size=True)
            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()
          
        elif map_event(ev, "input_set_end_marker_pos"):
        
            #Checks if Start Postion has been set yet and Sets Vars
            if self.start_marker_is_set == True:
                self.end_marker_pos = self.caret_pos - len(self.start_marker_text)
            else:
                self.end_marker_pos = self.caret_pos
            
            #Divide and recombine content with End Marker
            content = list(self.content.replace(self.end_marker_text,""))
            content.insert(self.caret_pos, self.end_marker_text) 
            content = "".join(content)
           
            #We know all else has been successful so we set this to True for Copy Code
            self.end_marker_is_set = True
           
            #Update Screen
            self.update_text(content, self.editable, check_size=True)
            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()
           
        elif map_event(ev, "input_select_all"):
            #Set Vars
            self.start_marker_pos = 0
            self.end_marker_pos = l
            content_removed_markers = self.remove_marker_text(self.content)
            content = "{0}{1}{2}".format(self.start_marker_text, content_removed_markers , self.end_marker_text)
           
            #We know all else has been successful so we set this to True for Copy Code
            self.start_marker_is_set = True
            self.end_marker_is_set = True
           
            #Update Screen
            self.update_text(content, self.editable, check_size=True)
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

