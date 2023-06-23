###
#
#   23Jun23 -  LH_1v2:  Just 1 MIDI CC controller for testing
#
###
import board
import usb_midi
import rotaryio
import adafruit_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff


# Rotary setup
encoder = rotaryio.IncrementalEncoder(board.GP28, board.VOLTAGE_MONITOR, 1)
last_position = 0


# Initialize the MIDI output
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)


while True:
    #Encoder loop

    knob1 = min(max(encoder.position, 0), 126)

    current_position = encoder.position
    position_change = current_position - last_position
    if position_change > 0:
        for _ in range(position_change):
            midi.send(ControlChange(16, knob1))
            knob1 = (knob1 +1)
            print("MIDI CC:", knob1, "     ", "Encoder Position:", encoder.position)
    elif position_change < 0:
        for _ in range(-position_change):
            midi.send(ControlChange(16, knob1))
            knob1 = (knob1 -1)
            print("MIDI CC:", knob1, "     ", "Encoder Position:", encoder.position)
    last_position = current_position