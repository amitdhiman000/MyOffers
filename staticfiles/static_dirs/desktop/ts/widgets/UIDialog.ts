import { UIOverlay } from "..";

export class UIDialog {
    show($html: any) {
        UIOverlay.Instance().show($html);
    }

    hide() {
        UIOverlay.Instance().hide();
    }

    close() {
        UIOverlay.Instance().close();
    }
};