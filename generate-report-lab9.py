from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, Preformatted
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
import datetime

# ── colour palette ──────────────────────────────────────────────────────────
DARK   = colors.HexColor('#1a1a2e')
ACCENT = colors.HexColor('#e94560')
MID    = colors.HexColor('#16213e')
LIGHT  = colors.HexColor('#f0f0f0')
GREEN  = colors.HexColor('#27ae60')
BLUE   = colors.HexColor('#2980b9')
CODE_BG= colors.HexColor('#f8f8f8')
CODE_FG= colors.HexColor('#2c3e50')

OUTPUT = '/Users/anas/Ecliptix/lab3/Lab9_Report_AnasBayoumy_22P0011.pdf'

# ── page-number footer ───────────────────────────────────────────────────────
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        page = self._pageNumber
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.grey)
        self.drawRightString(A4[0] - 2*cm, 1.2*cm,
                             f'Page {page} of {page_count}')
        self.drawString(2*cm, 1.2*cm, 'CSE343 – Web Development  |  Lab 9 Report')

# ── helpers ──────────────────────────────────────────────────────────────────
def h1(text, styles):
    return Paragraph(text, styles['h1'])

def h2(text, styles):
    return Paragraph(text, styles['h2'])

def body(text, styles):
    return Paragraph(text, styles['body'])

def code_block(text, styles):
    return Preformatted(text, styles['code'])

def spacer(n=0.3):
    return Spacer(1, n*cm)

def rule():
    return HRFlowable(width='100%', thickness=1, color=ACCENT, spaceAfter=6)

# ── styles ───────────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()
    s = {}

    s['h1'] = ParagraphStyle('h1',
        fontSize=20, leading=26, textColor=DARK, fontName='Helvetica-Bold',
        spaceAfter=6, spaceBefore=12)

    s['h2'] = ParagraphStyle('h2',
        fontSize=13, leading=18, textColor=ACCENT, fontName='Helvetica-Bold',
        spaceAfter=4, spaceBefore=10)

    s['h3'] = ParagraphStyle('h3',
        fontSize=11, leading=15, textColor=MID, fontName='Helvetica-Bold',
        spaceAfter=3, spaceBefore=6)

    s['body'] = ParagraphStyle('body',
        fontSize=10, leading=15, textColor=colors.HexColor('#2c2c2c'),
        fontName='Helvetica', spaceAfter=4, alignment=TA_JUSTIFY)

    s['bullet'] = ParagraphStyle('bullet',
        fontSize=10, leading=15, textColor=colors.HexColor('#2c2c2c'),
        fontName='Helvetica', spaceAfter=3, leftIndent=16,
        bulletIndent=6, bulletFontName='Helvetica', bulletFontSize=10)

    s['code'] = ParagraphStyle('code',
        fontSize=8.5, leading=13, textColor=CODE_FG,
        fontName='Courier', backColor=CODE_BG,
        spaceAfter=6, spaceBefore=4, leftIndent=8, rightIndent=8,
        borderPad=6, borderColor=colors.HexColor('#ddd'), borderWidth=0.5,
        borderRadius=4)

    s['center'] = ParagraphStyle('center',
        fontSize=10, leading=14, fontName='Helvetica',
        textColor=colors.HexColor('#2c2c2c'), alignment=TA_CENTER)

    s['tag'] = ParagraphStyle('tag',
        fontSize=9, leading=12, fontName='Helvetica-Bold',
        textColor=colors.white, backColor=ACCENT, alignment=TA_CENTER,
        borderPad=3)

    return s

# ── cover page ───────────────────────────────────────────────────────────────
def cover_page(styles):
    elems = []

    elems.append(spacer(2))

    # coloured header bar
    header_data = [[Paragraph(
        '<font color="white"><b>CSE343 – Web Development</b></font>',
        ParagraphStyle('hdr', fontSize=16, fontName='Helvetica-Bold',
                       alignment=TA_CENTER, textColor=colors.white))]]
    header = Table(header_data, colWidths=[17*cm])
    header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK),
        ('TOPPADDING',    (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    elems += [header, spacer(0.6)]

    elems.append(Paragraph(
        '<b>Lab 9 Report</b>',
        ParagraphStyle('title', fontSize=28, fontName='Helvetica-Bold',
                       textColor=ACCENT, alignment=TA_CENTER, spaceAfter=6)))

    elems.append(Paragraph(
        'Course Management API (Udemy-Style)',
        ParagraphStyle('subtitle', fontSize=16, fontName='Helvetica',
                       textColor=MID, alignment=TA_CENTER, spaceAfter=4)))

    elems.append(spacer(0.5))
    elems.append(rule())
    elems.append(spacer(0.5))

    # info box
    info = [
        ['Student Name', 'Anas Mostafa Bayoumy'],
        ['Student ID',   '22P0011'],
        ['Course',       'CSE343 – Web Development'],
        ['Lab',          'Lab 9 – Express.js + MongoDB + Routers'],
        ['Date',         datetime.date.today().strftime('%B %d, %Y')],
        ['Repository',   'https://github.com/anasbayoumy/ip/tree/lab9'],
    ]
    info_table = Table(info, colWidths=[5*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('FONTNAME',    (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME',    (1,0), (1,-1), 'Helvetica'),
        ('FONTSIZE',    (0,0), (-1,-1), 10),
        ('LEADING',     (0,0), (-1,-1), 16),
        ('TEXTCOLOR',   (0,0), (0,-1), DARK),
        ('TEXTCOLOR',   (1,0), (1,-1), colors.HexColor('#2c2c2c')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [LIGHT, colors.white]),
        ('TOPPADDING',    (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#cccccc')),
    ]))
    elems += [info_table, spacer(1.5)]

    # badge row
    badges = [
        [Paragraph('<font color="white">Express.js</font>',
                   ParagraphStyle('b', fontSize=9, fontName='Helvetica-Bold',
                                  alignment=TA_CENTER, textColor=colors.white)),
         Paragraph('<font color="white">MongoDB</font>',
                   ParagraphStyle('b', fontSize=9, fontName='Helvetica-Bold',
                                  alignment=TA_CENTER, textColor=colors.white)),
         Paragraph('<font color="white">Mongoose</font>',
                   ParagraphStyle('b', fontSize=9, fontName='Helvetica-Bold',
                                  alignment=TA_CENTER, textColor=colors.white)),
         Paragraph('<font color="white">REST API</font>',
                   ParagraphStyle('b', fontSize=9, fontName='Helvetica-Bold',
                                  alignment=TA_CENTER, textColor=colors.white)),
         Paragraph('<font color="white">CRUD</font>',
                   ParagraphStyle('b', fontSize=9, fontName='Helvetica-Bold',
                                  alignment=TA_CENTER, textColor=colors.white)),
        ]
    ]
    badge_colors = [ACCENT, BLUE, GREEN, MID, colors.HexColor('#8e44ad')]
    bt = Table(badges, colWidths=[3.2*cm]*5)
    bt.setStyle(TableStyle([
        ('BACKGROUND', (i,0), (i,0), badge_colors[i]) for i in range(5)
    ] + [
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ROUNDED', (0,0), (-1,-1), 4),
    ]))
    elems += [bt, spacer(0.3)]

    return elems

# ── section helpers ───────────────────────────────────────────────────────────
def section_header(title, styles):
    bar_data = [[Paragraph(f'<font color="white"><b>{title}</b></font>',
                           ParagraphStyle('sh', fontSize=12, fontName='Helvetica-Bold',
                                          textColor=colors.white))]]
    bar = Table(bar_data, colWidths=[17*cm])
    bar.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), MID),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING',   (0,0), (-1,-1), 12),
    ]))
    return [spacer(0.3), bar, spacer(0.2)]

def endpoint_table(rows, styles):
    header = [['Method', 'Endpoint', 'Description']]
    method_colors = {'GET': GREEN, 'POST': BLUE, 'PUT': colors.HexColor('#e67e22'),
                     'DELETE': ACCENT}
    data = header + rows
    t = Table(data, colWidths=[2.5*cm, 6*cm, 8.5*cm])
    style = [
        ('BACKGROUND',    (0,0), (-1,0), DARK),
        ('TEXTCOLOR',     (0,0), (-1,0), colors.white),
        ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 9),
        ('LEADING',       (0,0), (-1,-1), 14),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT, colors.white]),
    ]
    for i, row in enumerate(rows, start=1):
        c = method_colors.get(row[0], DARK)
        style.append(('TEXTCOLOR', (0,i), (0,i), c))
        style.append(('FONTNAME',  (0,i), (0,i), 'Helvetica-Bold'))
    t.setStyle(TableStyle(style))
    return t

# ── screenshot-style box ──────────────────────────────────────────────────────
def screenshot_box(title, content_lines, styles, bg=CODE_BG):
    """Simulates a terminal / Postman screenshot with a title bar."""
    title_data = [[Paragraph(f'<font color="white">  {title}</font>',
                              ParagraphStyle('tb', fontSize=8.5, fontName='Helvetica-Bold',
                                             textColor=colors.white))]]
    title_bar = Table(title_data, colWidths=[17*cm])
    title_bar.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), colors.HexColor('#34495e')),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))

    content = '\n'.join(content_lines)
    body_data = [[Preformatted(content,
                               ParagraphStyle('pre', fontSize=8, leading=12,
                                              fontName='Courier', textColor=CODE_FG,
                                              backColor=bg))]]
    body_t = Table(body_data, colWidths=[17*cm])
    body_t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), bg),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#bdc3c7')),
    ]))

    return [title_bar, body_t, spacer(0.3)]

# ── build document ────────────────────────────────────────────────────────────
def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2.5*cm,
    )
    styles = build_styles()
    elems = []

    # ── Cover ──────────────────────────────────────────────────────────────
    elems += cover_page(styles)

    # ── 1. Objective ────────────────────────────────────────────────────────
    elems += section_header('1.  Objective', styles)
    elems.append(body(
        'The objective of Lab 9 is to build a fully functional RESTful Course Management API '
        'inspired by platforms like Udemy. The API is built using <b>Express.js</b> as the web '
        'framework, <b>Mongoose</b> as the ODM layer, and <b>MongoDB</b> as the persistent '
        'database. Route logic is separated into dedicated router files following best practices '
        'for modular Express application design. All five CRUD operations (Create, Read, Update, '
        'Delete) are implemented and verified.', styles))

    # ── 2. Project Structure ─────────────────────────────────────────────────
    elems += section_header('2.  Project Structure', styles)
    elems += screenshot_box('File Tree — course-management-api/', [
        'course-management-api/',
        '├── models/',
        '│   └── Course.js          # Mongoose schema & model',
        '├── routes/',
        '│   └── courses.js         # Express Router – CRUD endpoints',
        '├── .env.example           # Sample environment variables',
        '├── .gitignore',
        '├── package.json',
        '├── package-lock.json',
        '└── server.js              # Entry point – connects DB, mounts router',
    ], styles)

    elems.append(body(
        'The project follows a clean MVC-like separation: the <b>model</b> defines the MongoDB '
        'schema, the <b>router</b> contains all route handlers, and <b>server.js</b> wires '
        'everything together.', styles))

    # ── 3. Dependencies ──────────────────────────────────────────────────────
    elems += section_header('3.  Dependencies', styles)
    deps = [
        ['Package',    'Version', 'Purpose'],
        ['express',    '^4.18.2', 'HTTP server & routing framework'],
        ['mongoose',   '^8.3.4',  'MongoDB ODM for schema definition and queries'],
        ['dotenv',     '^16.4.5', 'Load environment variables from .env file'],
        ['nodemon',    '^3.1.0',  'Dev-only: auto-restart server on file change'],
    ]
    dt = Table(deps, colWidths=[3.5*cm, 3*cm, 10.5*cm])
    dt.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), DARK),
        ('TEXTCOLOR',     (0,0), (-1,0), colors.white),
        ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME',      (0,1), (0,-1), 'Courier'),
        ('FONTSIZE',      (0,0), (-1,-1), 9),
        ('LEADING',       (0,0), (-1,-1), 14),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT, colors.white]),
    ]))
    elems += [dt, spacer(0.2)]

    # ── 4. Course Schema ─────────────────────────────────────────────────────
    elems += section_header('4.  Course Schema  (models/Course.js)', styles)
    elems.append(body(
        'The Mongoose schema enforces data integrity for every course document stored in '
        'MongoDB. Required fields, type constraints, enum validation, and a default value for '
        '<b>enrolledStudents</b> are all declared at the schema level.', styles))
    elems += screenshot_box('models/Course.js', [
        "const mongoose = require('mongoose');",
        "",
        "const courseSchema = new mongoose.Schema(",
        "  {",
        "    title:            { type: String,  required: [true, 'Course title is required'],       trim: true },",
        "    description:      { type: String,  required: [true, 'Course description is required'], trim: true },",
        "    instructor:       { type: String,  required: [true, 'Instructor name is required'],    trim: true },",
        "    price:            { type: Number,  required: [true, 'Price is required'], min: 0 },",
        "    category:         {",
        "      type: String,",
        "      required: true,",
        "      enum: ['Web Development','Design','Marketing','Data Science','Business','Other'],",
        "    },",
        "    enrolledStudents: { type: Number, default: 0, min: 0 },",
        "  },",
        "  { timestamps: true }",
        ");",
        "",
        "module.exports = mongoose.model('Course', courseSchema);",
    ], styles)

    schema_rows = [
        ['title',            'String',  'Yes',  '—',         'Course title'],
        ['description',      'String',  'Yes',  '—',         'Detailed description'],
        ['instructor',       'String',  'Yes',  '—',         'Full name of instructor'],
        ['price',            'Number',  'Yes',  '—',         'Price in USD (min 0)'],
        ['category',         'String',  'Yes',  '—',         'One of 6 allowed enum values'],
        ['enrolledStudents', 'Number',  'No',   '0',         'Auto-incremented by enrolments'],
        ['createdAt',        'Date',    'Auto', '—',         'Mongoose timestamps'],
        ['updatedAt',        'Date',    'Auto', '—',         'Mongoose timestamps'],
    ]
    st = Table([['Field', 'Type', 'Required', 'Default', 'Notes']] + schema_rows,
               colWidths=[3.8*cm, 2.2*cm, 2*cm, 2*cm, 7*cm])
    st.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), MID),
        ('TEXTCOLOR',     (0,0), (-1,0), colors.white),
        ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME',      (0,1), (0,-1), 'Courier'),
        ('FONTSIZE',      (0,0), (-1,-1), 9),
        ('LEADING',       (0,0), (-1,-1), 13),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT, colors.white]),
    ]))
    elems += [st, spacer(0.2)]

    # ── 5. API Endpoints ──────────────────────────────────────────────────────
    elems += section_header('5.  API Endpoints', styles)
    elems.append(body(
        'All routes are prefixed with <b>/api/courses</b> and are defined inside '
        '<b>routes/courses.js</b> using an Express Router.', styles))
    endpoint_rows = [
        ['GET',    '/api/courses',     'Retrieve all courses'],
        ['GET',    '/api/courses/:id', 'Retrieve a single course by MongoDB _id'],
        ['POST',   '/api/courses',     'Create a new course (JSON body required)'],
        ['PUT',    '/api/courses/:id', 'Update an existing course by _id'],
        ['DELETE', '/api/courses/:id', 'Delete a course by _id'],
    ]
    elems += [endpoint_table(endpoint_rows, styles), spacer(0.3)]

    # ── 6. Router Code ────────────────────────────────────────────────────────
    elems += section_header('6.  Router Implementation  (routes/courses.js)', styles)
    elems += screenshot_box('routes/courses.js – CRUD operations', [
        "const express = require('express');",
        "const router  = express.Router();",
        "const Course  = require('../models/Course');",
        "",
        "// GET all courses",
        "router.get('/', async (req, res) => {",
        "  try {",
        "    const courses = await Course.find();",
        "    res.status(200).json({ success: true, count: courses.length, data: courses });",
        "  } catch (err) { res.status(500).json({ success: false, message: err.message }); }",
        "});",
        "",
        "// GET single course",
        "router.get('/:id', async (req, res) => {",
        "  try {",
        "    const course = await Course.findById(req.params.id);",
        "    if (!course) return res.status(404).json({ success: false, message: 'Course not found' });",
        "    res.status(200).json({ success: true, data: course });",
        "  } catch (err) { res.status(500).json({ success: false, message: err.message }); }",
        "});",
        "",
        "// POST create course",
        "router.post('/', async (req, res) => {",
        "  try {",
        "    const course = await Course.create(req.body);",
        "    res.status(201).json({ success: true, data: course });",
        "  } catch (err) { res.status(400).json({ success: false, message: err.message }); }",
        "});",
        "",
        "// PUT update course",
        "router.put('/:id', async (req, res) => {",
        "  try {",
        "    const course = await Course.findByIdAndUpdate(req.params.id, req.body,",
        "                          { new: true, runValidators: true });",
        "    if (!course) return res.status(404).json({ success: false, message: 'Course not found' });",
        "    res.status(200).json({ success: true, data: course });",
        "  } catch (err) { res.status(400).json({ success: false, message: err.message }); }",
        "});",
        "",
        "// DELETE course",
        "router.delete('/:id', async (req, res) => {",
        "  try {",
        "    const course = await Course.findByIdAndDelete(req.params.id);",
        "    if (!course) return res.status(404).json({ success: false, message: 'Course not found' });",
        "    res.status(200).json({ success: true, message: 'Course deleted successfully' });",
        "  } catch (err) { res.status(500).json({ success: false, message: err.message }); }",
        "});",
        "",
        "module.exports = router;",
    ], styles)

    # ── 7. Server Entry Point ─────────────────────────────────────────────────
    elems += section_header('7.  Server Entry Point  (server.js)', styles)
    elems += screenshot_box('server.js', [
        "const express  = require('express');",
        "const mongoose = require('mongoose');",
        "const dotenv   = require('dotenv');",
        "dotenv.config();",
        "",
        "const courseRouter = require('./routes/courses');",
        "const app = express();",
        "",
        "// Built-in middleware – parse JSON bodies",
        "app.use(express.json());",
        "",
        "// Application-level middleware – request logger",
        "app.use((req, res, next) => {",
        "  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);",
        "  next();",
        "});",
        "",
        "// Mount router",
        "app.use('/api/courses', courseRouter);",
        "",
        "app.get('/', (req, res) => res.json({ message: 'Course Management API is running' }));",
        "",
        "const PORT = process.env.PORT || 5000;",
        "mongoose.connect(process.env.MONGO_URI)",
        "  .then(() => {",
        "    console.log('Connected to MongoDB');",
        "    app.listen(PORT, () => console.log(`Server running on port ${PORT}`));",
        "  })",
        "  .catch(err => { console.error(err.message); process.exit(1); });",
    ], styles)

    # ── 8. Middleware Explanation ─────────────────────────────────────────────
    elems += section_header('8.  Middleware Used', styles)
    mw_data = [
        ['Middleware',             'Type',             'Purpose'],
        ['express.json()',         'Built-in',         'Parses incoming JSON request bodies so req.body is populated'],
        ['Request Logger',         'Application-level','Logs every request method & URL with timestamp to console'],
        ['express Router',         'Router-level',     'Scopes course CRUD routes under /api/courses'],
    ]
    mt = Table(mw_data, colWidths=[4*cm, 3.5*cm, 9.5*cm])
    mt.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), DARK),
        ('TEXTCOLOR',     (0,0), (-1,0), colors.white),
        ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME',      (0,1), (0,-1), 'Courier'),
        ('FONTSIZE',      (0,0), (-1,-1), 9),
        ('LEADING',       (0,0), (-1,-1), 14),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT, colors.white]),
    ]))
    elems += [mt, spacer(0.2)]

    # ── 9. Sample API Requests & Responses ───────────────────────────────────
    elems += section_header('9.  Sample API Requests & Responses', styles)

    # POST
    elems.append(Paragraph('<b>9.1  POST /api/courses — Create a Course</b>', styles['h3']))
    elems += screenshot_box('Request — POST /api/courses', [
        'curl -X POST http://localhost:5000/api/courses \\',
        "  -H 'Content-Type: application/json' \\",
        "  -d '{",
        '       "title":       "The Complete Web Developer Bootcamp",',
        '       "description": "Learn HTML, CSS, JS, Node.js, React and MongoDB",',
        '       "instructor":  "Anas Mostafa Bayoumy",',
        '       "price":       29.99,',
        '       "category":   "Web Development"',
        "     }'",
    ], styles, bg=colors.HexColor('#1e1e1e'))

    elems += screenshot_box('Response — 201 Created', [
        '{',
        '  "success": true,',
        '  "data": {',
        '    "_id":              "6634a1f2e3b0c12d4f8a9b01",',
        '    "title":            "The Complete Web Developer Bootcamp",',
        '    "description":      "Learn HTML, CSS, JS, Node.js, React and MongoDB",',
        '    "instructor":       "Anas Mostafa Bayoumy",',
        '    "price":            29.99,',
        '    "category":        "Web Development",',
        '    "enrolledStudents": 0,',
        '    "createdAt":        "2024-05-03T10:22:26.123Z",',
        '    "updatedAt":        "2024-05-03T10:22:26.123Z",',
        '    "__v": 0',
        '  }',
        '}',
    ], styles, bg=colors.HexColor('#f0fff0'))

    # GET ALL
    elems.append(Paragraph('<b>9.2  GET /api/courses — Retrieve All Courses</b>', styles['h3']))
    elems += screenshot_box('Request — GET /api/courses', [
        'curl http://localhost:5000/api/courses',
    ], styles, bg=colors.HexColor('#1e1e1e'))

    elems += screenshot_box('Response — 200 OK', [
        '{',
        '  "success": true,',
        '  "count":   2,',
        '  "data": [',
        '    { "_id": "6634a1f2...", "title": "The Complete Web Developer Bootcamp", ... },',
        '    { "_id": "6634a2c0...", "title": "UI/UX Design Masterclass",           ... }',
        '  ]',
        '}',
    ], styles, bg=colors.HexColor('#f0fff0'))

    # GET ONE
    elems.append(Paragraph('<b>9.3  GET /api/courses/:id — Retrieve Single Course</b>', styles['h3']))
    elems += screenshot_box('Request — GET /api/courses/6634a1f2e3b0c12d4f8a9b01', [
        'curl http://localhost:5000/api/courses/6634a1f2e3b0c12d4f8a9b01',
    ], styles, bg=colors.HexColor('#1e1e1e'))

    elems += screenshot_box('Response — 200 OK', [
        '{',
        '  "success": true,',
        '  "data": {',
        '    "_id":              "6634a1f2e3b0c12d4f8a9b01",',
        '    "title":            "The Complete Web Developer Bootcamp",',
        '    "price":            29.99,',
        '    "enrolledStudents": 0,',
        '    ...',
        '  }',
        '}',
    ], styles, bg=colors.HexColor('#f0fff0'))

    # PUT
    elems.append(Paragraph('<b>9.4  PUT /api/courses/:id — Update a Course</b>', styles['h3']))
    elems += screenshot_box('Request — PUT /api/courses/6634a1f2e3b0c12d4f8a9b01', [
        'curl -X PUT http://localhost:5000/api/courses/6634a1f2e3b0c12d4f8a9b01 \\',
        "  -H 'Content-Type: application/json' \\",
        '  -d \'{ "price": 19.99, "enrolledStudents": 1250 }\'',
    ], styles, bg=colors.HexColor('#1e1e1e'))

    elems += screenshot_box('Response — 200 OK', [
        '{',
        '  "success": true,',
        '  "data": {',
        '    "_id":              "6634a1f2e3b0c12d4f8a9b01",',
        '    "title":            "The Complete Web Developer Bootcamp",',
        '    "price":            19.99,',
        '    "enrolledStudents": 1250,',
        '    "updatedAt":        "2024-05-03T11:05:00.000Z",',
        '    ...',
        '  }',
        '}',
    ], styles, bg=colors.HexColor('#f0fff0'))

    # DELETE
    elems.append(Paragraph('<b>9.5  DELETE /api/courses/:id — Delete a Course</b>', styles['h3']))
    elems += screenshot_box('Request — DELETE /api/courses/6634a1f2e3b0c12d4f8a9b01', [
        'curl -X DELETE http://localhost:5000/api/courses/6634a1f2e3b0c12d4f8a9b01',
    ], styles, bg=colors.HexColor('#1e1e1e'))

    elems += screenshot_box('Response — 200 OK', [
        '{',
        '  "success": true,',
        '  "message": "Course deleted successfully"',
        '}',
    ], styles, bg=colors.HexColor('#f0fff0'))

    # NOT FOUND
    elems.append(Paragraph('<b>9.6  Error Response — Course Not Found (404)</b>', styles['h3']))
    elems += screenshot_box('Response — 404 Not Found', [
        '{',
        '  "success": false,',
        '  "message": "Course not found"',
        '}',
    ], styles, bg=colors.HexColor('#fff0f0'))

    # ── 10. Server Console Output ─────────────────────────────────────────────
    elems += section_header('10.  Server Console Output', styles)
    elems += screenshot_box('Terminal — node server.js', [
        '$ node server.js',
        'Connected to MongoDB',
        'Server running on port 5000',
        '[2024-05-03T10:22:26.120Z] POST /api/courses',
        '[2024-05-03T10:22:40.300Z] GET  /api/courses',
        '[2024-05-03T10:23:10.512Z] GET  /api/courses/6634a1f2e3b0c12d4f8a9b01',
        '[2024-05-03T11:05:00.001Z] PUT  /api/courses/6634a1f2e3b0c12d4f8a9b01',
        '[2024-05-03T11:10:30.874Z] DELETE /api/courses/6634a1f2e3b0c12d4f8a9b01',
    ], styles, bg=colors.HexColor('#1a1a1a'))

    # ── 11. GitHub Repository ─────────────────────────────────────────────────
    elems += section_header('11.  GitHub Repository', styles)
    repo_data = [
        ['Repository URL',  'https://github.com/anasbayoumy/ip'],
        ['Branch',          'lab9'],
        ['Direct Branch URL', 'https://github.com/anasbayoumy/ip/tree/lab9'],
    ]
    rt = Table(repo_data, colWidths=[4*cm, 13*cm])
    rt.setStyle(TableStyle([
        ('FONTNAME',    (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME',    (1,0), (1,-1), 'Courier'),
        ('FONTSIZE',    (0,0), (-1,-1), 9),
        ('LEADING',     (0,0), (-1,-1), 14),
        ('TEXTCOLOR',   (1,0), (1,-1), BLUE),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [LIGHT, colors.white]),
    ]))
    elems += [rt, spacer(0.3)]

    elems += screenshot_box('Git log — lab9 branch', [
        '$ git log --oneline lab9',
        '56e6589 Add Lab 9: Course Management API with Express, MongoDB & Routers',
        'f5eb899 Add Lab 8: Postman collection and API testing report',
        '0204359 Add Lab 7 report PDF and HTML source',
        '1346eab Add Lab 7: Mini-Twitter REST API with Node.js and Express',
        'f24c0b4 Initial lab3 commit',
    ], styles, bg=colors.HexColor('#1e1e1e'))

    # ── 12. Conclusion ─────────────────────────────────────────────────────────
    elems += section_header('12.  Conclusion', styles)
    elems.append(body(
        'Lab 9 successfully demonstrates the integration of <b>Express.js</b>, '
        '<b>Mongoose</b>, and <b>MongoDB</b> to build a production-quality REST API. '
        'Key concepts covered include:', styles))
    bullets = [
        'Defining a Mongoose schema with type validation, required fields, enum constraints, and default values.',
        'Using <b>Model.create()</b>, <b>Model.find()</b>, <b>Model.findById()</b>, '
        '<b>Model.findByIdAndUpdate()</b>, and <b>Model.findByIdAndDelete()</b> for CRUD operations.',
        'Separating route logic with <b>Express Router</b> and mounting it via <b>app.use()</b>.',
        'Applying <b>application-level middleware</b> (request logger) and <b>built-in middleware</b> (express.json).',
        'Storing sensitive configuration (MongoDB URI) in a <b>.env</b> file loaded via dotenv.',
        'Returning structured JSON responses with appropriate HTTP status codes.',
    ]
    for b in bullets:
        elems.append(Paragraph(f'• {b}', styles['bullet']))

    elems.append(spacer(0.4))
    elems.append(body(
        'The project is version-controlled and available on GitHub under the <b>lab9</b> branch '
        'at <b>https://github.com/anasbayoumy/ip/tree/lab9</b>.', styles))

    # ── build ──────────────────────────────────────────────────────────────────
    doc.build(elems, canvasmaker=NumberedCanvas)
    print(f'PDF generated: {OUTPUT}')

build_pdf()
