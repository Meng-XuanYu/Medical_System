from django.http import JsonResponse

from MedicalSystem.view_funcs.base_user_funcs import fields_check


def get_instance(model_class, instance_id, instance_id_field):
    instance = model_class.objects.get(**{instance_id_field: instance_id})
    return instance


def get_all_instances(model_class):
    return model_class.objects.all()


def update_instance(model_class, data, instance_id, instance_id_field):
    # 检查字段有效性
    check_return = fields_check(model_class, data)
    if check_return is not None:
        return check_return

    instance = get_instance(model_class, instance_id, instance_id_field)

    if not instance:
        return JsonResponse({'status': 'error', 'message': f'{model_class.get_chinese_name()}不存在'}, status=404)

    instance.update_view_fields(data)

    return JsonResponse({'status': 'success', 'message': f'{model_class.get_chinese_name()}信息已更新'})
