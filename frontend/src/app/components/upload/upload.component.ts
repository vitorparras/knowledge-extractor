import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss']
})

export class UploadComponent {
  file: File | null = null;
  model: string = 'all'; // Modelo padrão
  loading: boolean = false; // Indicador de carregamento
  results: any = null; // Resultados do processamento

  constructor(private http: HttpClient) {}

  objectKeys = Object.keys;

  onFileSelected(event: any) {
    this.file = event.target.files[0];
  }

  uploadFile() {
    if (!this.file) {
      alert('Por favor, selecione um arquivo!');
      return;
    }

    this.loading = true; // Ativar o indicador de carregamento
    const formData = new FormData();
    formData.append('file', this.file);
    formData.append('model', this.model);

    this.http.post('http://localhost:5000/api/upload', formData).subscribe({
      next: (response: any) => {
        this.results = response; // Salvar resultados
        this.loading = false; // Desativar indicador de carregamento
      },
      error: (err) => {
        console.error('Erro no upload:', err);
        this.loading = false; // Desativar indicador de carregamento
      },
    });
  }
}