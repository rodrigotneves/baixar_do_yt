from pytube import YouTube

import re


def clean_filename(filename):
    # Substitui caracteres inválidos por underscores usando regex
    return re.sub(r'[^\w .\(\)-]', '_', filename)


def download_youtube_video_with_resolution(url, save_path, min_resolution=460):
    try:
        yt = YouTube(url)

        # Obtém a lista de streams disponíveis
        streams = yt.streams.filter(progressive=True, file_extension="mp4")
        print(streams)

        # Escolhe a stream com a resolução desejada
        selected_stream = None
        for stream in streams:
            print(stream)
            resolution = stream.resolution
            # print(resolution)
            if resolution and int(resolution[:-1]) >= min_resolution:
                selected_stream = stream
                break

        if selected_stream:
            # pegar o titulo do video
            title = yt.title
            title = clean_filename(title)
            title = title.strip()
            tamanho = selected_stream.filesize / 1024 / 1024
            tempo_estimado = tamanho * 8 / 100
            video_resolution = selected_stream.resolution

            # printar o tamanho do video
            print(f"Baixando {title} tamanho {tamanho:.2f} MB, Tempo estimado (100mbps) de: {tempo_estimado:.2f} minutos")  # noqa

            # Baixa o vídeo
            selected_stream.download(output_path=save_path, filename=f'{title}-{video_resolution}.mp4')  # noqa

            print(f"O vídeo {title} foi baixado com sucesso em videos/{title}")  # noqa
        else:
            print(
                f"Nenhuma stream com resolução maior ou igual a {min_resolution} encontrada."  # noqa
            )

    except Exception as e:
        print(f"Erro ao baixar o vídeo: {str(e)}")


if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=bZ8OaTcZARM"
    save_path = "videos"  # Defina o caminho onde você deseja salvar o vídeo  # noqa
    min_resolution = 460  # Escolha a resolução mínima desejada (por exemplo, 720)  # noqa

    download_youtube_video_with_resolution(youtube_url, save_path, min_resolution)  # noqa
