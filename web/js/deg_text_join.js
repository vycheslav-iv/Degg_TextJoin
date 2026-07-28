const { app } = window.comfyAPI.app;

const MAX_INPUTS = 20;

function findLastConnected(node) {
    let last = 0;
    for (const inp of node.inputs) {
        if (inp.name?.startsWith("text_") && inp.link) {
            const num = parseInt(inp.name.split("_")[1]);
            if (num > last) last = num;
        }
    }
    return last;
}

function rebuildInputs(node) {
    const lastConnected = findLastConnected(node);
    const targetCount = Math.min(lastConnected + 1, MAX_INPUTS);

    // Remove excess inputs from the end
    for (let i = node.inputs.length - 1; i >= 0; i--) {
        const inp = node.inputs[i];
        if (inp.name?.startsWith("text_")) {
            const num = parseInt(inp.name.split("_")[1]);
            if (num > targetCount) {
                node.removeInput(i);
            }
        }
    }

    // Add missing inputs
    for (let n = 1; n <= targetCount; n++) {
        const name = `text_${n}`;
        if (!node.inputs.find(i => i.name === name)) {
            node.addInput(name, "STRING");
        }
    }
}

app.registerExtension({
    name: "Degg.TextJoin",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "DeggTextJoin") return;

        const origOnNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            const ret = origOnNodeCreated?.apply(this, arguments);

            // Start with text_1 only
            rebuildInputs(this);

            return ret;
        };

        const onConnectionsChange = nodeType.prototype.onConnectionsChange;
        nodeType.prototype.onConnectionsChange = function (type, index, connected, link_info) {
            const ret = onConnectionsChange?.apply(this, arguments);

            if (type === 1) {
                setTimeout(() => {
                    rebuildInputs(this);
                }, 0);
            }

            return ret;
        };
    },
});
