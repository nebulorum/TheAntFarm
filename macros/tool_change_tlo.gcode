(The Ant Tool Change)
F@PROBE_FEED_FAST@
G53 G00 Z@SAFE_POS_Z@ F@PROBE_FEED_FAST@
@PROBE_TYPE_POS@
G00 X@PROBE_POS_X@ Y@PROBE_POS_Y@ F@PROBE_FEED_XY@
G54
@PROBE_HOLD_BEFORE@
G01 F@PROBE_FEED_SLOW@
G38.2 Z@PROBE_POS_MIN@
G01 F@PROBE_FEED_FAST@
G53 G00 Z@CHANGE_POS_Z@
G01 F@PROBE_FEED_XY@
G53 G00 X@CHANGE_POS_X@
G53 G00 Y@CHANGE_POS_Y@
M0
G53 G01 Z@SAFE_POS_Z@ F@PROBE_FEED_FAST@
@PROBE_TYPE_POS@
G01 F@PROBE_FEED_XY@
G00 X@PROBE_POS_X@ Y@PROBE_POS_Y@
G54
@PROBE_HOLD_BEFORE@
G01 F@PROBE_FEED_SLOW@
G38.2 Z@PROBE_POS_MIN@
G43.1 Z@TLO_TYPE_A@
G53 G01 Z@SAFE_POS_Z@ F@PROBE_FEED_FAST@
G54
G01 F@PROBE_FEED_XY@
G00 X@PRE_POS_X@ Y@PRE_POS_Y@
G01 F@PROBE_FEED_FAST@
G00 Z@PRE_POS_Z@
