import type { AssessmentResponse } from "../Types/types";


const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";


export class ApiError extends Error {}


export async function assessAudio(file: File): Promise<AssessmentResponse> {
    
   const form = new FormData();

   form.append("file", file);

   const response = await fetch(`${API_BASE}/api/assess`, {
     method: "POST",
     body: form,
   });


   if(!response.ok) {
      
    let detail = "Something went wrong while assessing this recording";

    try {
       const body = await response.json();
       if(body?.detail) detail = body.detail;
    } catch {
        
    }

    throw new ApiError(detail);

   }

   return response.json();



}
