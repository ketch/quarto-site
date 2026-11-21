-- Pandoc filter used when converting old (mostly Blogger-exported) HTML posts
-- to Markdown.  It removes presentational wrappers and dead scripts so the
-- result is plain, editable Markdown.

-- Unwrap <span> and <div> elements (font/style wrappers from Blogger),
-- keeping their contents.  Blogger marked inline code with a Courier
-- font span; those become inline code.
function Span(el)
  local style = (el.attributes["style"] or ""):lower()
  if style:find("courier") or style:find("monospace") then
    return pandoc.Code(pandoc.utils.stringify(el))
  end
  return el.content
end

function Div(el)
  return el.content
end

local function is_dead_raw(text)
  return text:find("cdn%.mathjax%.org") or text:find("x%-mathjax%-config")
end

-- Drop the old MathJax loader/config scripts (Quarto adds MathJax itself).
function RawBlock(el)
  if el.format == "html" and is_dead_raw(el.text) then
    return {}
  end
end

function RawInline(el)
  if el.format == "html" and is_dead_raw(el.text) then
    return {}
  end
end

-- Drop Blogger's 1x1 tracking pixel.
function Image(el)
  if el.src:find("blogger%.googleusercontent%.com/tracker") then
    return {}
  end
end
