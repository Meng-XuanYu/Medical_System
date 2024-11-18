from MedicalSystem.models import *
from django.forms.models import model_to_dict


def get_instance(model_class, **filters):
    """
    可能的报错：
    model_class.DoesNotExist：没有找到符合 filters 的实例
    model_class.MultipleObjectsReturned：查询结果中有多个符合条件的实例
    TypeError：传递的 filters 参数无效（如非关键字参数）或 filters 参数不是字典格式
    FieldError：filters 中包含模型中不存在的字段
    """
    # 调用模型类中的 prepare_data 方法处理 filters
    filters = model_class.prepare_data(filters)

    # 使用 **filters 解包多个属性作为查询条件
    instance = model_class.objects.get(**filters)
    User.objects.get(**filters)
    return instance


def get_instances(model_class, **filters):
    """
    可能的报错：
    TypeError：filters 参数不是字典格式
    FieldError：filters 中包含模型中不存在的字段
    """
    # 如果 filters 为空，返回所有实例
    if not filters:
        return model_class.objects.all()

    # 调用模型类中的 prepare_data 方法处理 filters
    filters = model_class.prepare_data(filters)

    # 根据 filters 查找匹配的实例列表
    return model_class.objects.filter(**filters)


def update_instance(model_class, filters, **updates):
    """
    可能的报错：
    model_class.DoesNotExist：没有找到符合 filters 的实例
    model_class.MultipleObjectsReturned：查询结果中有多个符合条件的实例
    AttributeError：使用 setattr() 更新不存在的字段
    ValueError：filters 中的字段名不正确（即模型中不存在该字段）
    IntegrityError：尝试保存对象时违反唯一性约束或其他数据库完整性规则
    FieldError：filters 中包含模型中不存在的字段
    """
    # 获取模型实例
    instance = get_instance(model_class, **filters)

    # 调用模型类中的 prepare_data 方法处理更新数据
    updates = model_class.prepare_data(updates)

    # 如果实例存在，则更新指定的属性
    for field, value in updates.items():
        setattr(instance, field, value)

    # 保存更改
    instance.save()


def add_instance(model_class, data):
    """
    可能的报错：
    IntegrityError：当数据不符合唯一约束或其他数据库完整性规则时
    FieldError：data 中包含模型中不存在的字段
    TypeError：data 参数不是字典格式
    ValueError：外键对应的实例不存在
    """
    # 调用模型类中的 prepare_data 方法处理更新数据
    data = model_class.prepare_data(data)

    model_class.objects.create(**data)


def delete_instance(model_class, **filters):
    """
    可能的报错：
    model_class.DoesNotExist：没有找到符合 filters 的实例
    model_class.MultipleObjectsReturned：查询结果中有多个符合条件的实例
    TypeError：传递的 filters 参数无效（如非关键字参数）或 filters 参数不是字典格式
    ValueError：filters 中的字段名不正确（即模型中不存在该字段）
    FieldError：filters 中包含模型中不存在的字段
    """
    # 调用模型类中的 prepare_data 方法处理 filters
    filters = model_class.prepare_data(filters)

    # 查找并删除符合条件的实例
    get_instance(model_class, **filters).delete()


MODEL_MAP = {
    'user': User,
    'staff': Doctor,
    'admin': Admin,
    'family': FamilyMember,
    'department': Department,
    'schedule': Schedule,
    'pharmacy': Pharmacy,
    'drug': Drug,
    'drugstock': DrugInventory,
    'examination': ExaminationArrangement,
    'examinationInfo': ExaminationInfo,
    'appointment': Appointment,
    'diagnosis': Diagnosis,
    'prescription': Prescription,
    'notification': Notification,
    'evaluation': Evaluation,
    'image': Image,
}


def instance_to_dict(instance):
    return model_to_dict(instance)
