#!/bin/bash

# Reset
Color_Off='\033[0m'       # Text Reset

# Regular Colors
Black='\033[0;30m'        # Black
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Blue='\033[0;34m'         # Blue
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan
White='\033[0;37m'        # White

# Bold
BBlack='\033[1;30m'       # Black
BRed='\033[1;31m'         # Red
BGreen='\033[1;32m'       # Green
BYellow='\033[1;33m'      # Yellow
BBlue='\033[1;34m'        # Blue
BPurple='\033[1;35m'      # Purple
BCyan='\033[1;36m'        # Cyan
BWhite='\033[1;37m'       # White

# Underline
UBlack='\033[4;30m'       # Black
URed='\033[4;31m'         # Red
UGreen='\033[4;32m'       # Green
UYellow='\033[4;33m'      # Yellow
UBlue='\033[4;34m'        # Blue
UPurple='\033[4;35m'      # Purple
UCyan='\033[4;36m'        # Cyan
UWhite='\033[4;37m'       # White

# Background
On_Black='\033[40m'       # Black
On_Red='\033[41m'         # Red
On_Green='\033[42m'       # Green
On_Yellow='\033[43m'      # Yellow
On_Blue='\033[44m'        # Blue
On_Purple='\033[45m'      # Purple
On_Cyan='\033[46m'        # Cyan
On_White='\033[47m'       # White

# High Intensity
IBlack='\033[0;90m'       # Black
IRed='\033[0;91m'         # Red
IGreen='\033[0;92m'       # Green
IYellow='\033[0;93m'      # Yellow
IBlue='\033[0;94m'        # Blue
IPurple='\033[0;95m'      # Purple
ICyan='\033[0;96m'        # Cyan
IWhite='\033[0;97m'       # White

# Italics
ItBlack='\033[3;90m'       # Black
ItRed='\033[3;91m'         # Red
ItGreen='\033[3;92m'       # Green
ItYellow='\033[3;93m'      # Yellow
ItBlue='\033[3;94m'        # Blue
ItPurple='\033[3;95m'      # Purple
ItCyan='\033[3;96m'        # Cyan
ItWhite='\033[3;97m'       # White

# Bold High Intensity
BIBlack='\033[1;90m'      # Black
BIRed='\033[1;91m'        # Red
BIGreen='\033[1;92m'      # Green
BIYellow='\033[1;93m'     # Yellow
BIBlue='\033[1;94m'       # Blue
BIPurple='\033[1;95m'     # Purple
BICyan='\033[1;96m'       # Cyan
BIWhite='\033[1;97m'      # White

# High Intensity backgrounds
On_IBlack='\033[0;100m'   # Black
On_IRed='\033[0;101m'     # Red
On_IGreen='\033[0;102m'   # Green
On_IYellow='\033[0;103m'  # Yellow
On_IBlue='\033[0;104m'    # Blue
On_IPurple='\033[0;105m'  # Purple
On_ICyan='\033[0;106m'    # Cyan
On_IWhite='\033[0;107m'   # White

ARG=$ICyan
CMD=$BRed
HLP=$ItWhite
LNK=$UBlue
HDG=$BWhite
ENDARG=$Color_Off
ENDCMD=$Color_Off
ENDHLP=$Color_Off
ENDLNK=$Color_Off
ENDHDG=$Color_Off

usage_message="${HDG}usage:${ENDHDG} ${CMD}./meera.sh <command>${ENDCMD} ${ARG}[<args>]${ENDARG}

${HDG}These are commands used in various situations:${ENDHDG}

${HDG}install MEERA as fresh installation${ENDHDG}
   ${CMD}clean${ENDCMD}                                ${HLP}Clean the project directory${ENDHLP}
   ${CMD}pre-install${ENDCMD}                          ${HLP}Prepare machine for installation${ENDHLP}
   ${CMD}install${ENDCMD}                              ${HLP}Install MEERA${ENDHLP}
   ${CMD}deploy${ENDCMD} ${ARG}[server|telegram-client|all]${ENDARG}  ${HLP}Deploys MEERA. Takes an optional argument to deploy specific component. Defaults to 'all'${ENDHLP}

${HDG}manipulate machine learning model${ENDHDG}
   ${CMD}train${ENDCMD} ${ARG}[<iterations>]${ENDARG}                 ${HLP}Train ML models. Takes optional argument to specify number of training iterations. Defaults to 50${ENDHLP}
   ${CMD}evaluate${ENDCMD}                             ${HLP}Evaluate ML models${ENDHLP}
   ${CMD}download-model${ENDCMD}                       ${HLP}Downloads ML models${ENDHLP}
   ${CMD}install-model${ENDCMD}                        ${HLP}Install backup models stored in download folder during training${ENDHLP}

${HDG}code quality and sanity checks${ENDHDG}
   ${CMD}lint${ENDCMD}                                 ${HLP}Lint code for code quality${ENDHLP}
   ${CMD}test${ENDCMD}                                 ${HLP}Run tests${ENDHLP}

For more info visit ${LNK}http://www.ameykamat.in/MEERA/${ENDLNK}
"

echo -e "$usage_message"