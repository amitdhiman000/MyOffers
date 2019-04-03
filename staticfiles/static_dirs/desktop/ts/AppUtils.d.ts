export declare class ObjectUtil {
    private static _instance;
    static Instance(): ObjectUtil;
    type(o: any): any;
    isArray(o: any): boolean;
    isObject(o: any): boolean;
    merge(a1: any, a2: any): any;
    dump(obj: any): void;
}
export declare class AppUtil {
    private static _instance;
    private _name;
    static Instance(): AppUtil;
    csrfToken(): {};
    csrfField(): string;
    name(): string;
}
export declare class Event {
    _set: any;
    sub(p: any): void;
    unsub(p: any): void;
    trigger(e: any): boolean;
}
export declare class Cookie {
    private static _instance;
    static Instance(): Cookie;
    get(cname: string): any;
    set(cname: string, cvalue: string, exdays: number): void;
    has(cname: string): boolean;
}
export declare class Storage {
    private static _instance;
    static Instance(): Storage;
    get(key: string): string;
    set(key: string, val: string): void;
}
