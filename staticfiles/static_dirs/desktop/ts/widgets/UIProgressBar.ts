export class UIProgressBar {
    $_ui: any = null;
    constructor(title: string, btnText: string) {
        this.$_ui = `<div class="wt-progress-outer" >
                    <div class="wt-progress-inner">
                    <div class="wt-progress-filename">${title}</div>
                    <div class="wt-progress-bar">&nbsp;0%</div></div>
                    <div class="wt-progress-control">
                    <button class="ui-btn">${btnText}</button>
                    </div></div>`;
    }

    show($parent: any) {
        $parent.append(this.$_ui);
        this.$_ui.show();
    }
};