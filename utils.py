def calc_imc (weight:float,height:float):
    
    # IMC = weight/height^2
    value = round(weight/(height*height),2)

    if value < 16.9:
        result = 'Muito abaixo do peso'
        comment = '...'
    elif value >= 17 and value <= 18.4:
        result = 'Abaixo do peso'
        comment = '...'
    elif value >= 18.5 and value <= 24.9:
        result = 'Peso ideal/normal'
        comment = '...'
    elif value >= 25 and value <= 29.9:
        result = 'Acima do peso'
        comment = '...'
    elif value >= 30 and value <= 34.9:
        result = 'Obesidade grau 1'
        comment = '...'
    elif value >= 35 and value <= 40:
        result = 'Obesidade grau 2'
        comment = '...'
    elif value >= 40:
        result = 'Obesidade grau 3'
        comment = '...'
    else:
        value = 0
        result = 'error'
        comment = 'error, invalid inputs'

    return {'value':value,'result':result,'comment':comment}