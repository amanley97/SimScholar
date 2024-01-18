import inspect, sys
import gem5.components as cmp

def get_cls(file, mask):
    cls = []
    for name, obj in inspect.getmembers(file):
        if inspect.isclass(obj) and name != mask:
            cls.append(name)
    return cls

# print(inspect.getclasstree(cmp))

classes = [cls_name for cls_name, cls_obj in inspect.getmembers(sys.modules['gem5.components.memory']) if inspect.isclass(cls_obj)]
print(classes)
