import { WebCamera as _WebCamera } from 'https://esm.sh/@shivantra/react-web-camera?deps=react@19.0,react-dom@19.0&external=react,react-dom';
import {fileToBase64} from 'https://esm.sh/filetobase64';
import {
    Camera,
    ArrowRepeat
} from 'https://esm.sh/react-bootstrap-icons?deps=react@19.0,react-dom@19.0&external=react,react-dom';

export default function WebCamera(props, context) {
    const cameraHandler = React.useRef(null);
    const onCaptureRef = React.useRef(props.onCapture);

    if (onCaptureRef.current != props.onCapture) {
        onCaptureRef.current = props.onCapture;
    }
    delete props.onCapture;

    async function handleCapture() {
        const file = await cameraHandler.current?.capture();
        if (file) {
            if (onCaptureRef.current && typeof onCaptureRef.current === "function") {
                fileToBase64(file, (base64) => {
                    onCaptureRef.current(base64);
                });
            } else {
                const ObjectURL = URL.createObjectURL(file);
                const link = document.createElement("a");
                link.href = ObjectURL;
                link.download = file.name || "capture.png";
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }
        }
    }

    function handleSwitch() {
        cameraHandler.current?.switch();
    }

    props.ref = cameraHandler;

    return React.createElement("div", {style: {position: "relative"}}, [
        React.createElement(_WebCamera, props),
        React.createElement(
            "button", 
            {
                onClick: handleCapture, 
                style: {position: "absolute", bottom: 20, right: "50%", left: "50%", width: "4em"}
            }, 
            [
                React.createElement(Camera, {size: "3em"}),
            ]
        ),
        React.createElement(
            "button", 
            {
                onClick: handleSwitch, 
                style: {position: "absolute", top: 10, right: 10}
            }, 
            [
                React.createElement(ArrowRepeat, {size: "2em"}),
            ]
        )
    ]);
}