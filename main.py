from typing import List
from utils import *
from components import *
from state import *
from math import log2
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 90
INI_TICK = FPS

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
WIDTH = screen.get_width()
HEIGHT = screen.get_height()
pygame.display.set_caption('DigiSim')
running = True
font = pygame.font.SysFont('Monospace', 20)
font_small = pygame.font.SysFont('Monospace', 16)
clock = pygame.time.Clock()
components = List[Button]
draggables = []
isDragged = False
wiring = WiringState.IDLE
current_wire = None
wire_line = None
mouseOffset = (0, 0)
not_gates = 0
and_gates = 0
ortho = False
titleButtons: List[Button] = []
gates: List[GateEnclosure] = []
ios: List[Node] = []
wires: List[CircuitWire] = []
clocks: List[Clock] = []
textInputs: List[InputBox] = []
customGateButtons: List[Button] = []
stateSaver = StateSaver()

def add_node(x: int, y: int, mode):
  global ios
  found_obst = False
  for inp in ios:
    if inp.x == x and inp.y == y:
      add_node(x + 25 if x + 40 < WIDTH else 10, y + 5, mode)
      found_obst = True
      break
  if not found_obst:
    n = Node(x, y, mode, font)
    ios.append(n)

def createBtnFromState(state, x, y):
  add_custom_btn = Button(state['name'], x, y, 'gray', font)
  def add_custom_gate(event):
    print(f'custom {state["name"]}')
    global gates
    _s = None
    for _g in stateSaver.data:
      if _g['name'] == state['name']:
        _s = _g
        break
    
    if _s is None:
      return
    outs = len(_s['outputs'][0])
    inps = int(log2(len(_s['outputs'])))
    _inputs = [Wire(IO()) for _ in range(inps)]
    _outputs = [Wire(IO()) for _ in range(outs)]
    a = StateGate(state['name'], _inputs, _outputs)
    g = GateEnclosure(a, state['name'], 80, 50, font)
    gates.append(g)
  add_custom_btn.onClick = add_custom_gate
  
  return add_custom_btn

cumWidth = 0
add_inp_btn = Button('Add Input Node', cumWidth, 0, 'gray', font)
def add_input_node(event):
  add_node(10, 90, 'input')
add_inp_btn.onClick = add_input_node

cumWidth += add_inp_btn.rect.width
add_out_btn = Button('Add Output Node', cumWidth, 0, 'gray', font)
def add_output_node(event):
  global ios
  add_node(WIDTH - 30, 90, 'output')
add_out_btn.onClick = add_output_node

cumWidth += add_out_btn.rect.width
add_and_btn = Button('And', cumWidth, 0, 'gray', font)
def add_and_gate(event):
  global gates
  global and_gates
  a = AND(Wire(IO()), Wire(IO()), Wire(IO()))
  g = GateEnclosure(a, f'a_{and_gates + 1}', 80, 50, font)
  and_gates += 1
  gates.append(g)
add_and_btn.onClick = add_and_gate

cumWidth += add_and_btn.rect.width
add_not_btn = Button('Not', cumWidth, 0, 'gray', font)
def add_not_gate(event):
  global gates
  global not_gates
  a = NOT(Wire(IO()), Wire(IO()))
  g = GateEnclosure(a, f'n_{not_gates + 1}', 80, 50, font)
  not_gates += 1
  gates.append(g)
add_not_btn.onClick = add_not_gate

cumWidth += add_not_btn.rect.width
add_clk_btn = Button('Clock', cumWidth, 0, 'gray', font)
def add_clk_obj(event):
  global clocks
  clk = Clock(70, 70, font, INI_TICK, FPS)
  if len(clocks) != 0:
    clk.sync(clocks[-1])
    clocks.append(clk)
  else:
    clocks = [clk]
    # __n = Node(-100, -100, 'input', font)
    # __n.setIO(clk.getIO())
    # ios.append(__n)

add_clk_btn.onClick = add_clk_obj

cumWidth += add_clk_btn.rect.width
add_wire_btn = Button('Add Wire', cumWidth, 0, 'gray', font)
def add_wire(event):
  global wiring
  if wiring == WiringState.IDLE:
    wiring = True
    add_wire_btn.setLabel('Esc', keep_dims=True)
    add_wire_btn.render(keep_dims=True)
    wiring = WiringState.START
  else:
    global current_wire
    current_wire = None
    wiring = WiringState.IDLE
    add_wire_btn.setLabel('Add Wire')
    add_wire_btn.render()
add_wire_btn.onClick = add_wire

cumWidth += add_wire_btn.rect.width
save_btn = Button('Save', cumWidth, 0, 'gray', font)
def save_gate(event):
  global ios
  global gates
  global wires
  global textInputs
  inp = None
  if len(textInputs) == 0:
    inp = InputBox(WIDTH // 2 - 40, HEIGHT // 2 - 15, 80, 30, font)
    textInputs.append(inp)
  else:
    inp = textInputs[0]

  inp.active = True

  inps = [_n for _n in ios if _n.mode == 'input']
  outs = [_n for _n in ios if _n.mode == 'output']
  def _save():
    global ios
    global gates
    global wires
    global textInputs
    global stateSaver
    state = State(inp.text, gates, inps, outs)
    stateSaver.save(state)
    ios = []
    gates = []
    wires = []
    textInputs = []
    # stateSaver.load()
  
  inp.when_done_typing(_save)

save_btn.onClick = save_gate

cumWidth += save_btn.rect.width
exit_btn = Button('Exit', cumWidth, 0, 'gray', font)
def quit_game(event):
  global running
  running = False

exit_btn.onClick = quit_game

titleButtons = [add_inp_btn, add_out_btn, add_and_btn, add_not_btn, add_clk_btn, add_wire_btn, save_btn, exit_btn]

sec_row_h = exit_btn.height

def draw_cust_buttons():
  global cumWidth
  global customGateButtons
  cumWidth = 0
  customGateButtons = []
  for _btn in stateSaver.data:
    cust_btn = createBtnFromState(_btn, cumWidth, sec_row_h)
    customGateButtons.append(cust_btn)
    cumWidth += cust_btn.rect.width

draw_cust_buttons()

while running:
  for event in pygame.event.get():
    x, y = pygame.mouse.get_pos()
    if isDragged:
      for d in draggables:
        if d['mode'] == 'nw':
          d['comp'].setPos(x - d['offset'][0], y - d['offset'][1])
        elif d['mode'] == '_from':
          d['comp'].move_start(x - d['offset'][0], y - d['offset'][1])
        elif d['mode'] == '_to':
          d['comp'].move_end(x - d['offset'][0], y - d['offset'][1])
    if event.type == pygame.QUIT:
      running = False

    if event.type == pygame.KEYUP:
      if event.key == pygame.K_LSHIFT:
        ortho = False

    if event.type == pygame.KEYDOWN:
      for textBox in textInputs:
        if textBox.active:
          textBox.handle_event(event)

      if event.key == pygame.K_w:
        wiring = WiringState.IDLE
        add_wire(event)
      if event.key == pygame.K_DOWN:
        if len(clocks) == 0:
          INI_TICK = 2 * INI_TICK
        else:
          tkr = clocks[0].ticker
          for clk in clocks:
            clk.setTick(tkr * 2)
      if event.key == pygame.K_UP:
        if len(clocks) == 0:
          INI_TICK = INI_TICK // 2
        else:
          tkr = clocks[0].ticker
          for clk in clocks:
            clk.setTick(tkr // 2)
      if event.key == pygame.K_LSHIFT:
        ortho = True
      if event.key == pygame.K_BACKSPACE:
        first_clock = False
        for ind, comp in enumerate(clocks):
          if comp.rect.collidepoint(x, y):
            try:
              clocks.remove(comp)
            except ValueError:
              pass
            else:
              if ind == 0:
                first_clock = True
                break
        
        if first_clock and len(clocks) > 0:
          clocks[0].is_sync = False
          for j in range(len(clocks) - 1):
            clocks[j + 1].sync(clocks[0])


        for comp in ios:
          if comp.rect.collidepoint(x, y):
            for w in comp.wires:
              try:
                wires.remove(w)
                del w
              except ValueError:
                pass
            try:
              ios.remove(comp)
            except ValueError:
              pass

        for comp in gates:
          if comp.rect.collidepoint(x, y):
            for w in comp.wires:
              try:
                wires.remove(w)
              except ValueError:
                pass
            try:
              gates.remove(comp)
            except ValueError:
              pass
            if comp.gate.__class__ == AND:
              and_gates -= 1
            else:
              not_gates -= 1 
              
        
    if event.type == pygame.VIDEORESIZE:
      WIDTH = screen.get_width()
      HEIGHT = screen.get_height()
    
    if event.type == pygame.MOUSEBUTTONDOWN:
      if pygame.mouse.get_pressed()[0]:
        found_top = False

        # for textBox in textInputs:
        #   if not textBox.rect.collidepoint(x, y) and textBox.active:
        #     textBox.active = False

        for comp in ios:
          if comp.rect.collidepoint(x, y):
            if wiring == WiringState.START:
              current_wire = Wire(comp.io)
              wiring = WiringState.END
              wire_line = CircuitWire(x, y)
              comp.add_wire(wire_line)
            elif wiring == WiringState.END:
              l = Line(wire_line.get_end(), (x, y), 2, 'black', ortho)
              wire_line.add_wire(l)
              comp.add_wire(wire_line)
              wires.append(wire_line)
              wire_line = None
              comp.io = current_wire.getIO()
              add_wire_btn.onClick(event)
              wiring = WiringState.IDLE
              add_wire_btn.render()
            else:
              if len(draggables) == 0 or found_top:
                comp.onClick(event)
              
              if not found_top:
                found_top = True
                
                mouseOffset = (x - comp.x, y - comp.y)
                draggables.append({
                  'comp': comp,
                  'offset': mouseOffset,
                  'mode': 'nw'
                })
                isDragged = True
                for w in wires:
                  if comp.rect.collidepoint(w.x, w.y):
                    draggables.append({
                    'comp': w,
                    'offset': (x - w.x, y - w.y),
                    'mode': '_from'
                    })
                  elif comp.rect.collidepoint(w.endx, w.endy):
                    draggables.append({
                    'comp': w,
                    'offset': (x - w.endx, y - w.endy),
                    'mode': '_to'
                    })

        
        for comp in clocks:
          if comp.rect.collidepoint(x, y):
            if wiring == WiringState.START:
              _col = comp.isNode(x, y)
              if _col:
                current_wire = Wire(comp.getIO())
                wiring = WiringState.END
                wire_line = CircuitWire(x, y)
            elif wiring == WiringState.END:
              _col = comp.isNode(x, y)
              if _col:
                l = Line(wire_line.get_end(), (x, y), 2, 'black', ortho)
                wire_line.add_wire(l)
                wires.append(wire_line)
                wire_line = None
                comp.setOutput(current_wire.getIO())
                add_wire_btn.onClick(event)
                wiring = WiringState.IDLE
                add_wire_btn.render()
            else:
              if not found_top:
                found_top = True
                isDragged = True
                mouseOffset = (x - comp.x, y - comp.y)
                draggables.append({
                  'comp': comp,
                  'offset': mouseOffset,
                  'mode': 'nw'
                })
                for w in wires:
                  if comp.isNode(w.x, w.y):
                    draggables.append({
                    'comp': w,
                    'offset': (x - w.x, y - w.y),
                    'mode': '_from'
                    })
                  elif comp.isNode(w.endx, w.endy):
                    draggables.append({
                    'comp': w,
                    'offset': (x - w.endx, y - w.endy),
                    'mode': '_to'
                    })


        for comp in titleButtons:
          if comp.rect.collidepoint(x, y):
            comp.onClick(event)

        for comp in customGateButtons:
          if comp.rect.collidepoint(x, y):
            comp.onClick(event)
        
        for comp in gates:
          if comp.rect.collidepoint(x, y):
            if wiring == WiringState.START:
              i_ind = comp.getInpIndex(x, y)
              o_ind = comp.getOutIndex(x, y)
              if i_ind != -1:
                current_wire = Wire(comp.gate.inputs[i_ind].getIO())
                comp.gate.setInput(i_ind, current_wire)
                wiring = WiringState.END
                wire_line = CircuitWire(x, y)
                comp.add_wire(wire_line)
              elif o_ind != -1:
                current_wire = Wire(comp.gate.outputs[o_ind].getIO())
                comp.gate.setOutput(o_ind, current_wire)
                wiring = WiringState.END
                wire_line = CircuitWire(x, y)
                comp.add_wire(wire_line)
            elif wiring == WiringState.END:
              i_ind = comp.getInpIndex(x, y)
              o_ind = comp.getOutIndex(x, y)
              if i_ind != -1:
                l = Line(wire_line.get_end(), (x, y), 2, 'black', ortho)
                wire_line.add_wire(l)
                wires.append(wire_line)
                comp.add_wire(wire_line)
                wire_line = None
                comp.gate.setInput(i_ind, current_wire)
                add_wire_btn.onClick(event)
                wiring = WiringState.IDLE
                add_wire_btn.render()
              elif o_ind != -1:
                l = Line(wire_line.get_end(), (x, y), 2, 'black', ortho)
                wire_line.add_wire(l)
                wires.append(wire_line)
                comp.add_wire(wire_line)
                wire_line = None
                comp.gate.setOutput(o_ind, current_wire)
                add_wire_btn.onClick(event)
                wiring = WiringState.IDLE
                add_wire_btn.render()
            else:
              if not found_top:
                found_top = True
                isDragged = True
                mouseOffset = (x - comp.x, y - comp.y)
                draggables.append({
                  'comp': comp,
                  'offset': mouseOffset,
                  'mode': 'nw'
                })
                for w in wires:
                  if comp.getInpIndex(w.x, w.y) != -1 or comp.getOutIndex(w.x, w.y) != -1:
                    draggables.append({
                    'comp': w,
                    'offset': (x - w.x, y - w.y),
                    'mode': '_from'
                    })
                  elif comp.getInpIndex(w.endx, w.endy) != -1 or comp.getOutIndex(w.endx, w.endy) != -1:
                    draggables.append({
                    'comp': w,
                    'offset': (x - w.endx, y - w.endy),
                    'mode': '_to'
                    })

      
      if wire_line is not None:
        p = pygame.mouse.get_pos()
        if wire_line.get_end() != p:
          l = Line(wire_line.get_end(), p, 2, 'black', ortho)
          wire_line.add_wire(l)

    if event.type == pygame.MOUSEBUTTONUP:
      draggables = []
      isDragged = False

  if stateSaver.loaded:
    draw_cust_buttons()
    stateSaver.loaded = False

  screen.fill((128,128,128))
  for line in wires:
    line.render(screen)
  if wiring == WiringState.END:
    wire_line.draw_temp(pygame.mouse.get_pos(), ortho)
    wire_line.render(screen)

  for comp in clocks:
    comp.compute()
    comp.render()
    screen.blit(comp.surface, (comp.x, comp.y))
  for comp in titleButtons:
    screen.blit(comp.surface, (comp.x, comp.y))
  for comp in customGateButtons:
    screen.blit(comp.surface, (comp.x, comp.y))
  
  _inp_count = 0
  _out_count = 0
  for comp in ios:
    _before = False
    n = 0
    if comp.mode == 'input':
      n = _inp_count
      _inp_count += 1
      _before = True
    else:
      n = _out_count
      _out_count += 1
    comp.render(n, font_small, _before)
    screen.blit(comp.surface, (comp.x, comp.y))
  for comp in gates:
    comp.gate.compute()
    comp.render()
    screen.blit(comp.surface, (comp.x, comp.y))
  for comp in textInputs:
    comp.update()
    comp.render(screen)
  pygame.display.update()
  clock.tick(FPS)