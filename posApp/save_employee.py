
def save_product(request):
    save_product = Products()
    data =  request.POST
    resp = {'status':'failed'}
    id= ''
    
    if 'id' in data:
        id = data['id']
    if id.isnumeric() and int(id) > 0:
        check = Products.objects.exclude(id=id).filter(code=data['code']).all()
    else:
        check = Products.objects.filter(code=data['code']).all()
    if len(check) > 0 :
        resp['msg'] = "Employee Code Already Exists in the database"
    else:
       
        try:
            image_file = request.FILES.get('image')
            id = data.get('id')
            code = data.get('code')
            category_id = data.get('category')
            name = data.get('name')
            description = data.get('description')
            price = data.get('price')
            status = data.get('status')
            quantity = data.get('quantity')
           
            if (data['id']).isnumeric() and int(data['id']) > 0 :
           
                save_product = Products.objects.get(id=id)
                save_product.code = code
                save_product.category_id=category_id 
                save_product.name = name 
                save_product.description = description 
                save_product.price = price
                save_product.status = status
                save_product.quantity = quantity
                
             
            if image_file:
                 
                # Delete old image file if exists                
               
                if save_product.image:
                    default_storage.delete(Products.image.path)
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
                status=status
                
                
            )
                                     
                if image_file:
                   
                    save_product.image = image_file
            

                    save_product.save()
            resp['status'] = 'success'
            messages.success(request, 'Employee Successfully saved.')
        except:
            resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


