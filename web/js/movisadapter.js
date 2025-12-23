import { app } from '../../../scripts/app.js'
import { api } from '../../../scripts/api.js'

// Cloud specific auth code. Short circuits if not on cloud
async function getAuthHeader() {
    try {
        const authStore = await api.getAuthStore?.()
        return authStore ? await authStore.getAuthHeader() : null
    } catch (error) {
        console.warn('Failed to get auth header:', error)
        return null
    }
}

async function uploadFile(file, progressCallback) {
    try {
        // Wrap file in formdata so it includes filename
        const body = new FormData();
        const i = file.webkitRelativePath?.lastIndexOf('/') ?? -1;
        const subfolder = i > 0 ? file.webkitRelativePath.slice(0, i + 1) : '';
        const new_file = new File([file], file.name, {
            type: file.type,
            lastModified: file.lastModified,
        });
        body.append("image", new_file);
        if (i > 0) {
            body.append("subfolder", subfolder);
        }
        const url = api.apiURL("/upload/image")
        const resp = await new Promise((resolve) => {
            let req = new XMLHttpRequest()
            req.upload.onprogress = (e) => progressCallback?.(e.loaded / e.total)
            req.onload = () => resolve(req)
            req.open('post', url, true)
            getAuthHeader().then((headers) => {
                headers ??= {}
                for (const key in headers)
                    req.setRequestHeader(key, headers[key])
                req.send(body)
            })
        })

        if (resp.status !== 200) {
            alert(resp.status + " - " + resp.statusText);
        }
        return resp
    } catch (error) {
        alert(error);
    }
}

function addUploadWidget(nodeType, nodeData, widgetName, type = "video") {
    const video_extensions = ["video/webm", "video/mp4", "video/x-matroska", "image/gif", "video/avi", "video/x-msvideo"];
    const accept = { 'video': video_extensions };

    function chainCallback(object, property, callback) {
        if (object == undefined) {
            console.error("Tried to add callback to non-existent object")
            return;
        }
        if (property in object && object[property]) {
            const callback_orig = object[property]
            object[property] = function () {
                const r = callback_orig.apply(this, arguments);
                return callback.apply(this, arguments) ?? r
            };
        } else {
            object[property] = callback;
        }
    }

    chainCallback(nodeType.prototype, "onNodeCreated", function () {
        const node = this
        const pathWidget = this.widgets.find((w) => w.name === widgetName);
        
        if (!pathWidget) {
            console.warn(`Widget ${widgetName} not found on node`);
            return;
        }

        const fileInput = document.createElement("input");
        chainCallback(this, "onRemoved", () => {
            fileInput?.remove();
        });

        async function doUpload(file) {
            let resp = await uploadFile(file, (p) => node.progress = p)
            node.progress = undefined
            if (resp.status != 200) {
                return false
            }
            const filename = JSON.parse(resp.responseText).name;
            if (!pathWidget.options.values.includes(filename)) {
                pathWidget.options.values.push(filename);
            }
            pathWidget.value = filename;
            if (pathWidget.callback) {
                pathWidget.callback(filename)
            }
            return true
        }

        Object.assign(fileInput, {
            type: "file",
            accept: accept[type].join(','),
            style: "display: none",
            onchange: async () => {
                if (fileInput.files.length) {
                    return await doUpload(fileInput.files[0])
                }
            },
        });

        // Handle drag and drop
        this.onDragOver = (e) => !!e?.dataTransfer?.types?.includes?.('Files')
        this.onDragDrop = async function (e) {
            if (!e?.dataTransfer?.types?.includes?.('Files')) {
                return false
            }
            const item = e.dataTransfer?.files?.[0]
            if (accept[type].includes(item?.type)) {
                return await doUpload(item)
            }
            return false
        }

        document.body.append(fileInput);
        
        let uploadWidget = this.addWidget("button", "choose " + type + " to upload", "image", () => {
            // Clear the active click event
            app.canvas.node_widget = null
            fileInput.click();
        });
        uploadWidget.options.serialize = false;
    });
}

// Register the extension
app.registerExtension({
    name: "MovisAdapter.FileUpload",
    
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // Upload widget functionality removed - ImagesToVideo node accepts IMAGE input directly
    },
});

