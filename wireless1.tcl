# ======================================================================
# Read input file for data
# Input file contains the following information in order:
# 1. Number of nodes
# 2. X dimension of simulation area
# 3. Y dimension of simulation area
# 4. Simulation time
# 5. Seed
# ======================================================================

set fp [open "input.txt" r]
set file_data [read $fp]
set data [split $file_data "\n"]

set i 1

foreach line $data {
set data_$i $line
   incr i
}

# ======================================================================
# Define options
# ======================================================================

set val(chan)       Channel/WirelessChannel
set val(prop)       Propagation/TwoRayGround
set val(netif)      Phy/WirelessPhy
set val(mac)        Mac/802_11
set val(ifq)        CMUPriQueue
set val(ll)         LL
set val(ant)        Antenna/OmniAntenna
set val(x)              $data_2   ;# X dimension of the topography
set val(y)              $data_3   ;# Y dimension of the topography
set val(ifqlen)         50            ;# max packet in ifq
set val(seed)           $data_5
set val(adhocRouting)   DSR
set val(nn)             $data_1             ;# how many nodes are simulated
set val(cp)             "cbr-test" 
set val(sc)             "scen-test" 
set val(stop)           $data_4           ;# simulation time

# Setting the Transmission range by fixing Rx threshold and CS threshold

$val(chan) set CSThresh_ 1.76149e-10 ; # Carrier sense range is 300
$val(chan) set RxThresh_ 3.65262e-10 ; # Transmission range is 250

# =====================================================================
# Main Program
# ======================================================================

# Create simulator instance
set ns_		[new Simulator]
$ns_ use-newtrace
# Setup topography object
set topo	[new Topography]

# Create trace object for ns and nam
set tracefd	[open wireless-out.tr w]
set namtrace [open wireless-out.nam w]

$ns_ trace-all $tracefd
$ns_ namtrace-all-wireless $namtrace $val(x) $val(y)

# Define topology
$topo load_flatgrid $val(x) $val(y)

# Create God object
set god_ [create-god $val(nn)]

# Global node setting
$ns_ node-config -adhocRouting $val(adhocRouting) \
                 -llType $val(ll) \
                 -macType $val(mac) \
                 -ifqType $val(ifq) \
                 -ifqLen $val(ifqlen) \
                 -antType $val(ant) \
                 -propType $val(prop) \
                 -phyType $val(netif) \
                 -channelType $val(chan) \
                 -topoInstance $topo \
                 -agentTrace ON \
                 -routerTrace OFF \
                 -macTrace OFF 

#  Create the specified number of nodes [$val(nn)] and "attach" them
#  to the channel. 

for {set i 0} {$i < $val(nn) } {incr i} {
   set node_($i) [$ns_ node]	
   $node_($i) random-motion 0		;# disable random motion
}
 
# Define node movement model
puts "Loading connection pattern..."
source $val(cp)
# Define traffic model
puts "Loading scenario file..."
source $val(sc)

# Log node movements

set opt(nn) $val(nn)

proc log-movement {} {

   global logtimer ns_ ns
   set ns $ns_
   source /home/khushboo/ns-allinone-2.35/ns-2.35/tcl/mobility/timer.tcl

   Class LogTimer -superclass Timer
   LogTimer instproc timeout {} {
   
      global opt node_;
      for {set i 0} {$i < $opt(nn)} {incr i} {
        $node_($i) log-movement
      }

      $self sched 1
   }

   set logtimer [new LogTimer]
   $logtimer sched 1

}


# Define node initial position in nam
for {set i 0} {$i < $val(nn)} {incr i} {
# 30 defines the node size in nam, must adjust it according to your scenario
#The function must be called after mobility model is defined

   $ns_ initial_node_pos $node_($i) 30
}

# Tell nodes when the simulation ends
for {set i 0} {$i < $val(nn) } {incr i} {
   $ns_ at $val(stop).0 "$node_($i) reset";
}

$ns_ at  $val(stop).0002 "puts \"NS EXITING...\" ; $ns_ halt"

puts "Starting Simulation..."
$ns_ at 0.0 "log-movement"
$ns_ run
