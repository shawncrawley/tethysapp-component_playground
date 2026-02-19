import _Editor from "https://esm.sh/@monaco-editor/react/?deps=react@19.0,react-dom@19.0"

function debounce(func, timeout = 750) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => { func.apply(this, args); }, timeout);
    }
}

export default function Editor(props, context) {
    if (props.onChange) {
        let originalOnChange = props.onChange;
        if (props.onChange.name === "safeEventHandler") {
            props.onChange = debounce((a, b) => originalOnChange(a, b))
        }
    }
    return React.createElement(_Editor, props);
}
