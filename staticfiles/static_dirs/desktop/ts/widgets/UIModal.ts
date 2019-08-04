import { UIOverlay } from "..";

/* App Modal */
export class UIModal {
    show($html: any, options?: any): this {
        UIOverlay.Instance().show($html, { closeOnClickOutside:true, onClose: this.onClose});
        return this;
    }

    update($html: any): this {
        UIOverlay.Instance().update($html);
        return this;
    }

    hide(): this {
        UIOverlay.Instance().hide();
        return this;
    }

    close(): this {
        UIOverlay.Instance().close();
        return this;
    }

    onClose(e: any) {

    }
};