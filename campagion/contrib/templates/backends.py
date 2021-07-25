from django.template.backends.django import DjangoTemplates, Template, reraise, TemplateDoesNotExist
from django.template.context import make_context
from django.template.engine import Engine
from django.template.loader_tags import ExtendsNode

class CustomBackend(DjangoTemplates):
    def from_string(self, template_code):
        return CustomTemplate(self.engine.from_string(template_code))

    def get_template(self, template_name):
        try:
            return CustomTemplate(self.engine.get_template(template_name), self)
        except TemplateDoesNotExist as exc:
            reraise(exc, self)


class CustomTemplate(Template):
    def get_filled_blocks(self):
        nodes = self.template.nodelist.get_nodes_by_type(ExtendsNode)
        if len(nodes) == 0:
            return []
        blocks = []
        for node in nodes:
            for block in node.blocks.values():
                if len(block.nodelist) != 0:
                    blocks.append(block.name)
        return blocks
    
    def render(self, context=None, request=None):
            context['FILLED_BLOCKS'] = self.get_filled_blocks()
            context = make_context(context, request, autoescape=self.backend.engine.autoescape)
            try:
                return self.template.render(context)
            except TemplateDoesNotExist as exc:
                reraise(exc, self.backend)