/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ClosePosPopup } from "@point_of_sale/app/navbar/closing_popup/closing_popup";
import { rpc } from "@web/core/network/rpc";

patch(ClosePosPopup.prototype, {
    setup() {
        super.setup();
        this.attachment = null;
        this.attachmentFilename = null;
    },

    onAttachment(ev) {
        const file = ev.target.files[0];
        if (file) {
            this.attachment = file;
            this.attachmentFilename = file.name;
            console.log("Selected attachment:", file.name);
        }
    },

    async closeSession() {
        if (this.attachment) {
            try {
                const base64 = await this._fileToBase64(this.attachment);

                const result = await rpc("/web/dataset/call_kw", {
                    model: "pos.session",
                    method: "save_closing_attachment",
                    args: [],
                    kwargs: {
                        attachment_data: base64,
                        filename: this.attachmentFilename
                    }
                });

                console.log("Attachment saved:", result);

            } catch (error) {
                console.error("Error saving attachment:", error);
            }
        }
        return super.closeSession();
    },

    _fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsArrayBuffer(file);

            reader.onload = () => {
                const bytes = new Uint8Array(reader.result);
                let binary = '';
                for (let i = 0; i < bytes.byteLength; i++) {
                    binary += String.fromCharCode(bytes[i]);
                }
                const base64 = btoa(binary);
                resolve(base64);
            };

            reader.onerror = error => reject(error);
        });
    },

    downloadAttachment(orderId, filename) {
        const url = `/web/content/pos.order/${orderId}/attachment/${filename}?download=true`;
        window.open(url, "_blank");
    }
});
