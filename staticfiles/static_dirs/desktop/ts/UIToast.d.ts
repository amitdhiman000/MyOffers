export declare class UIToast {
    private static _instance;
    constructor();
    static Instance(): UIToast;
    show(text?: string, timeout?: number): any;
    hide(): any;
}
