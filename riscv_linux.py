import m5
from m5.objects import Root

from gem5.utils.requires import requires
from gem5.components.boards.riscv_board import RiscvBoard
from gem5.components.memory import DualChannelDDR4_2400
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.simulate.simulator import Simulator
from gem5.resources.workload import Workload

from gem5.resources.workload import CustomWorkload
from gem5.resources.resource import AbstractResource
from gem5.resources.resource import CustomResource, CustomDiskImageResource, DiskImageResource

# This runs a check to ensure the gem5 binary is compiled for RISCV.

requires(isa_required=ISA.RISCV)

# With RISCV, we use simple caches.
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)

# Here we setup the parameters of the l1 and l2 caches.
cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
    l1d_size="16kB", l1i_size="16kB", l2_size="256kB"
)

# Memory: Dual Channel DDR4 2400 DRAM device.

memory = DualChannelDDR4_2400(size="3GB")

# Here we setup the processor. We use a simple processor.
processor = SimpleProcessor(
    cpu_type=CPUTypes.TIMING, isa=ISA.RISCV, num_cores=2
)

# Here we setup the board. The RiscvBoard allows for Full-System RISCV
# simulations.
board = RiscvBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

#board.set_workload(CustomResource(local_path="/home/shc/projects/riscv-imgs/ubuntudene/ubuntu-22.04.3-preinstalled-server-riscv64+unmatched.img"))

#board.set_kernel_disk_workload(kernel=CustomResource("/home/shc/projects/riscv-imgs/ubuntu/bootloader-vmlinux-5.10"), disk_image=CustomDiskImageResource("/home/shc/projects/riscv-imgs/ubuntudene/ubuntu-22.04.3-preinstalled-server-riscv64+unmatched.img"))


board.set_workload(CustomWorkload(
    function = "set_kernel_disk_workload",
    parameters = {
        #"bootloader" : AbstractResource("/home/shc/projects/riscv-imgs/ubuntu/bootloader-vmlinux-5.10"),
        "kernel" : CustomResource("/home/shc/.cache/gem5/riscv-bootloader-vmlinux-5.10"),
        "disk_image" : CustomDiskImageResource("/home/shc/.cache/gem5/riscv-ubuntu-20.04-img", root_partition="1") ## metadata?
        #"disk_image" : DiskImageResource("/home/shc/projects/riscv-imgs/ubuntudene/ubuntu-22.04.3-preinstalled-server-riscv64+unmatched.img")
    }
))


#board.set_workload(Workload("riscv-ubuntu-20.04-boot"))

simulator = Simulator(board=board)
simulator.run()

