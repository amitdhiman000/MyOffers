export declare class HttpResponseHandler {
    progress_up: (p: number) => any;
    progress_dn: (p: number) => any;
    complete: (s: any, d: any) => any;
    constructor(handlers: any);
}
export declare class HttpService {
    _handle: any;
    constructor();
    abort(): any;
    get(url: string, data: any, callback: any): any;
    post(url: string, data: any, callback: any): any;
    file(url: string, data: any, handler: any): any;
    request(handler: any, options: any): any;
    private _request;
}
