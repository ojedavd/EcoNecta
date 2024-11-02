import { Observable } from 'rxjs';
import { Subject } from 'rxjs';
import { Injectable } from '@angular/core';

@Injectable()
export class LoadingController {

    private loadingSubject: Subject<boolean> = new Subject<boolean>();
    private calls: number = 0;

    get onLoading(): Observable<boolean> {
        return this.loadingSubject.asObservable();
    }

    private set toggle(value: boolean) {
        this.loadingSubject.next(value);
    }

    show(): void {
        this.calls++;
        this.toggle = true;
    }

    hide(): void {
        if (!this.calls) { return; }
        this.calls--;
        this.toggle = false;
    }
}
