#old save products
def save_product(request):
    save_product = Products()
    data =  request.POST
    resp = {'status':'failed'}
    id= ''
    image_file = request.FILES.get('image')
    if 'id' in data:
        id = data['id']
    if id.isnumeric() and int(id) > 0:
        check = Products.objects.exclude(id=id).filter(code=data['code']).all()
    else:
        check = Products.objects.filter(code=data['code']).all()
    if len(check) > 0 :
        resp['msg'] = "Product Code Already Exists in the database"
    else:
        category = Category.objects.filter(id = data['category_id']).first()
        
        try:
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                save_product = Products.objects.filter(id = data['id']).update(code=data['code'], category_id=category, name=data['name'], description = data['description'], price = float(data['price']),cost = float(data['cost']),status = data['status'])
            if image_file:
                # If there is an existing image, delete it
                if save_product.image:
                    save_product.image = image_file
                save_product.save()
            else:
                save_product = Products(code=data['code'], category_id=category, name=data['name'], description = data['description'], price = float(data['price']),cost = float(data['cost']),status = data['status'])
                
            if image_file:
                # If there is an existing image, delete it
                if save_product.image:
                    save_product.delete(save_product.image.path)

                # Save the new image file
                save_product.image = image_file
                save_product.save()
                # Save the image file to the media directory
                save_product.image.save(save_product.code + '.jpg', image_file, content_type='image/jpeg')
                
                resp['status'] = 'success'
                resp['filename'] = save_product.code + '.jpg'
                resp['content_type'] = 'image/jpeg'
                resp['content_length'] = save_product.image.size
            else:
                resp['status'] = 'success'
                messages.success(request, 'Product has been saved successfully.')
        except:
            resp['status'] = 'failed'
            messages.success(request, 'Product has failed to save.')
    return HttpResponse(json.dumps(resp), content_type="application/octet-stream")

#new save products
def save_product(request):
    save_product = Products()
    data =  request.POST
    resp = {'status':'failed'}
    id= ''
    
    if 'id' in data:
        id = data['id']
        code = data['code']
        
    if id.isnumeric() and int(id) > 0:
        check = Products.objects.exclude(id=id).filter(code=data['code']).all()
    else:
        check = Products.objects.filter(code=data['code']).all()
    if len(check) > 0 :
        resp['msg'] = "Products Code Already Exists in the database"
    else:
       
        try:
            image_file = request.FILES.get('image')
            Products_id = data.get('id')
            code = data.get('code')
            category_id = data.get('category')
            name = data.get('name')
            description = data.get('description')
            price = data.get('price')
            cost = data.get('cost')
            status = data.get('status')

           
            if (data['id']).isnumeric() and int(data['id']) > 0 :
           
                save_product = Products.objects.get(id=Products_id)
                save_product.code = code
                save_product.category_id=category_id 
                save_product.name = name 
                save_product.description = description 
                save_product.price = price
                save_product.cost = cost
                save_product.status = status
                
             
            if image_file:
                 
                # Delete old image file if exists                
               
                if save_product.image:
                    default_storage.delete(save_product.image.path)
                # Save new image file
                save_product.image = image_file
                
                save_product.save()
                
                    
            else:
               
                save_product = Products(
                code=code,
                category_id=category_id,
                name=name,
                description=description,
                price=price,
                cost=cost,
                status=status
                
            )
                                     
                if image_file:
                   
                    save_product.image = image_file
            

            save_product.save()
            resp['status'] = 'success'
            messages.success(request, 'Products Successfully saved.')
        except:
            resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

