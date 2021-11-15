from . import Ultra_Light, BaseBlock_1_PythonSyntax

def Start(HW_id):
    if HW_id in [1738]:
        Ultra_Light.Start(HW_id)
    elif HW_id == 1739:
        BaseBlock_1_PythonSyntax.test