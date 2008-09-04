Audacious Plugin Caveats
------------------------

1. If the UADE plugin for audacious does not appear to play an Amiga file
formats, then ensure the following is DISABLED:

Preferences -> Audio -> Format Detection -> Detect file formats by extenstion


2. If sound appears to stutter or contains intermittent pauses (in particular
   this seems to apply if you are using the pulseaudio output driver) then
   adjust the buffer size to around 500. You may need to experiment on your
   system

Preferences -> Audio -> Buffer size


