from bokeh.core.properties import String
from bokeh.models import Button, LayoutDOM

IMPL = """
import * as p from "core/properties"
import {LayoutDOM, LayoutDOMView} from "models/layouts/layout_dom"

export class FileInputView extends LayoutDOMView
  initialize: (options) ->
    super(options)
    input = document.createElement("input")
    input.type = "file"
    input.onchange = () =>
      @model.value = input.value
    @el.appendChild(input)

export class FileInput extends LayoutDOM
  default_view: FileInputView
  type: "FileInput"
  @define {
    value: [ p.String ]
  }
"""

class FileInput(LayoutDOM):
    __implementation__ = IMPL
    value = String()


