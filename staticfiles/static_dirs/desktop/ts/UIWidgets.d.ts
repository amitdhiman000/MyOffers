export declare class UIOverlay {
    _shown: boolean;
    $overlay: any;
    $closebtn: any;
    $body: any;
    $html: any;
    $html_def: any;
    _options_def: any;
    _options: any;
    init(): void;
    _apply_options(options: any): void;
    shown(): boolean;
    show($html?: any, options?: {}): this;
    hide(): this;
    update($html: any): this;
    clear(): this;
    close(e: any): void;
    _close(e: any): void;
    _onclose(e: any): void;
    _onclick(e: any): void;
    _onkeyup(e: any): void;
}
export declare class UIModal extends UIOverlay {
    show($html: any): void;
}
export declare class UIOptionList {
    _name: string;
    _count: number;
    _selectedIndex: number;
    _jsonItemsList: null;
    _config: any;
    _overrides: any;
    _scrollTimer: any;
    $_self: any;
    $_list: any;
    $_selectedItem: any;
    constructor($Inst: any, config: any, overrides: any);
    _create(e: any): void;
    _destroy(e: any): void;
    _onfocus(e: any): void;
    _onunfocus(e: any): void;
    source(key: string, respCB: any): void;
    itemCreate(item: any): any;
    onItemSelect($input: any, item: any): void;
    onEnter($input: any, item: any): void;
    _ondata(jsonItemsList: any): void;
    _setItemSelected(newIndex: number): void;
    _onlistscroll(e: any): void;
    _onitemhover(e: any): void;
    _onitemclick(e: any): void;
    _notifyItemSelected(): void;
    _onkeypress(e: any): void;
    _onkeyup(e: any): void;
}
