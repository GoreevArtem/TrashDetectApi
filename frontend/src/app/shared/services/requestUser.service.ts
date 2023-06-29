import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { environment } from "src/app/environment";

@Injectable()
export class RequestUserService {
    constructor(private http: HttpClient){}
    private path1='request/create_request';
    private path2='request/get_all_requests';
    private path3='request/get_request';

    createRequest(data:any)
    {
        const httpOptions = {headers: new HttpHeaders({'Content-Type':'application/json','Authorization':`Bearer ${localStorage.getItem('t')}`})}; 
        return this.http.post<any>(`${environment.api}${this.path1}`,data,httpOptions);
    }

    getRequests(limit: number)
    {
        let params = `?limit=${limit}`;
        const httpOptions = {headers: new HttpHeaders({'Content-Type':'application/json','Authorization':`Bearer ${localStorage.getItem('t')}`})}; 
        return this.http.get<any>(`${environment.api}${this.path2}`+params,httpOptions);
    }

    getRequest(id: number)
    {
        let params = `?req_id=${id}`;
        const httpOptions = {headers: new HttpHeaders({'Content-Type':'application/json','Authorization':`Bearer ${localStorage.getItem('t')}`})}; 
        return this.http.get<any>(`${environment.api}${this.path3}`+params,httpOptions);
    }

 
}