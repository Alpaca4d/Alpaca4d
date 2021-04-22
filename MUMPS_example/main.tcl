wipe
set process_id [getPID]

model basic -ndm 3 -ndf 6
# source definitions
source definitions.tcl
# source materials
source materials.tcl
# source sections
source sections.tcl
# source node
source nodes.tcl
# source element
source elements.tcl
# source analysis_steps
source analysis_steps.tcl

wipe
