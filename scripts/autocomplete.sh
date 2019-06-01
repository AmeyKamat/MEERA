_script()
{
	_script_commands="clean pre-install install download-model install-model lint train evaluate test deploy help"
	_deploy_commands="server telegram-client all"

    local cur prev

    cur=${COMP_WORDS[COMP_CWORD]}
    prev=${COMP_WORDS[COMP_CWORD-1]}

    case ${COMP_CWORD} in
        1)
            COMPREPLY=($(compgen -W "${_script_commands}" -- ${cur}))
            ;;
        2)
            case ${prev} in
                deploy)
                    COMPREPLY=($(compgen -W "${_deploy_commands}" -- ${cur}))
                    ;;
                *)
                    COMPREPLY=()
                    ;;
            esac
            ;;
        *)
            COMPREPLY=()
            ;;
    esac
}

complete -F _script ./meera.sh