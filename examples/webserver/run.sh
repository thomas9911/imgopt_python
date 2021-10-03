#! /bin/bash

start() {
    poetry update
    FLASK_APP=webserver:new_app FLASK_ENV=development poetry run flask run -p 5050
}

fmt() {
    poetry run black .
}

print_help() {
    echo "Usage: $0 {start|fmt|help}"
    echo "                 (by default does start)"
    echo "commands:"
    echo "    start:"
    echo "                 run the server"
    echo "    fmt:"
    echo "                 run formatter"
    echo "    help:"
    echo "                 prints this text"
    echo
}

if [ -z $(which poetry) ]; then
    echo "ERROR: this example requires poetry to be installed"
    exit 1
fi

case "$1" in
start)
    start
    ;;

fmt)
    fmt
    ;;

help|h|--help|-h)
    print_help
    exit 1
    ;;

*)
    start
    ;;
esac
