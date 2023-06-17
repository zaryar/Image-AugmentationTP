from neural_style import stylize2



def style_filter(path, style, outputpath):
    path_to_model = {
        
        "anime": "local_version/back/fast_neural_style/saved_models/anime.pth",
        "candy": "local_version/back/fast_neural_style/saved_models/candy.pth",
        "feininger":"local_version/back/fast_neural_style/saved_models/feini.pth",
        "monet":"local_version/back/fast_neural_style/saved_models/monet.pth",
        "mosaic": "local_version/back/fast_neural_style/saved_models/mosaic.pth",
        "rain_princess":"local_version/back/fast_neural_style/saved_models/rain_princess.pth",
        "starry_night": "local_version/back/fast_neural_style/saved_models/starry_night.pth",
        "udnie": "local_version/back/fast_neural_style/saved_models/udnie.pth"
    }
    model_path = path_to_model[style]
    stylize2(path,model_path,outputpath)



style_filter("local_version/back/fast_neural_style/images/content-images/vaile.png","anime","local_version/back/fast_neural_style/images/output-images/stylefiltertest.jpg")
