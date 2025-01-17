# 答辩讲稿 --并不严肃的 README--太太太他妈肝了！！

<代码熟练度还是不够，很多问题都得现学>

## 创新点

### 1. `Flask` 框架

- 足够轻量级的 Web 框架，适用于简单项目快速落地。
- 使用 `Python` 语言开发
### 2. `Blueprint` 结构

- 蓝图功能支持`map`和`metro`两个模块。
- 高扩展、低耦合：`app`文件夹下新建子文件夹，注入项目即可加入功能，不需要考虑其他模块功能的冲突。

### 3. `Bootstrapt` UI 组件

- UI 组件模块化，方便管理和调用
- 快捷的 CDN 链接导入形式
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
```
### 4. `basic` 统一管理

- 占位符操作，模板语法提高代码复用性

### 5. `constants.py`

- 常量的统一集中宏定义
- 便于集中替换 `API_KEY`、`FOOTER` 等常量

### 6. `SQLAlchemy` 数据库操作和 `SOLite` 数据库

- 轻量化数据库配置
- 迁移工具：表结构变更（e.g. 要加字段，可以快速迁移，也可以回退版本）

### 7. `Jinja2` 模板引擎

- locations变量的传参，循环遍历数据库，把每一个都创建出来.

```jinja2
  // 坐标
  {% for location in locations %}
    var lng = {{ location.lng }};
    var lat = {{ location.lat }};
    var address = "{{ location.address }}";
    var tag = "{{ location.tag }}";

    var point = new BMapGL.Point(lng, lat);
    var marker = new BMapGL.Marker(point);
    map.addOverlay(marker);

    // 信息窗口
    var opts = {
        width: 200,
        height: 100,
        title: tag
    };
```

## 已解决的典型问题


### 1. 前后通讯的问题

通过 `GET` 和 `POST` 信号量来分支前端的请求

### 2. 多个左键点击事件冲突

我查阅了百度地图 api 的类参考文档，想要通过在左键点击事件里通过 if else 条件分支区分左键点击事件不同的行为，但是在官方 api 文档里没找到合适的类和方法，就改用右键点击事件添加任意点坐标，这样相比于左键不容易误触。

使用闭包？
```jinja2
// map.html
// 使用闭包确保每个标记的点击事件都有自己的信息
(function(marker, point, address, lng, lat) {
    var infoWindow = new BMapGL.InfoWindow('{{constants.ADDRESS}}：' + address + '<br/>{{constants.LNG}}：' + lng + '<br/>{{constants.LAT}}：' + lat, opts);
    marker.addEventListener('click', function () {
        map.openInfoWindow(infoWindow, point);
    });
})(marker, point, address, lng, lat);
{% endfor %}
```


### 3. 图层覆盖

以导航栏为例，通过引入代码：

```html
style="z-index: 999;
```

来设置图层的优先级

```html
<!-- map.html -->
<div id="keywordSearch" style="z-index: 999; margin-top: 80px" class="d-flex align-items-start ms-3" role="search">
```

## 后续改进

### 1. 行政区划的开关

### 2. WTF的工具：用python代码validate验证表单


## 工具解析

### 1. **Flask 框架**
Flask 是一个轻量级的 Python Web 框架，它非常适合小型到中型的 Web 应用。Flask 提供了路由、请求处理、模板渲染等基本功能，可以让开发者专注于业务逻辑而无需处理复杂的配置。

在本项目中，Flask 被用来：
- 作为应用的核心框架来处理路由和请求。
- 利用模板引擎 Jinja2 渲染动态 HTML 页面。
- 提供 Flask-WTF 用于处理表单验证和输入。

### 2. **SQLAlchemy：数据库操作**
`SQLAlchemy` 是一个强大的数据库工具包，它提供了一个对象关系映射 (ORM) 功能，使得 Python 对象和数据库中的表之间的交互变得简洁易懂。它支持多种数据库，如 MySQL、PostgreSQL、SQLite 和 MariaDB。

在本项目中，我们使用 SQLAlchemy 来操作数据库，包括：
- 定义模型类（如 `Location` 类），这些类映射到数据库中的表。
- 使用 SQLAlchemy 的查询 API 来插入、查询和删除数据。
- 实现对象与数据库表之间的自动映射，使得操作数据库时不需要编写原始 SQL 语句。

在 `Location` 模型中，每个字段（如经度、纬度、地址和标签）都通过 SQLAlchemy 的 `Column` 来定义。通过设置 `nullable=False`，我们确保每个字段都不能为空。


#### `Location` 类
`Location` 是表示地点信息的模型类，包含以下字段：
- `lng`：表示地点的经度（浮动值）。
- `lat`：表示地点的纬度（浮动值）。
- `address`：地点的描述地址（字符串类型）。
- `tag`：标签，方便对地点进行分类（字符串类型）。

`Location` 类的构造函数初始化了这些字段，并且 `__repr__` 和 `__str__` 方法提供了调试和打印类实例的方式。

### 3. **Flask-WTF：表单处理**
`Flask-WTF` 是 Flask 的一个扩展，它封装了 `WTForms`，使得表单的创建、验证和提交变得非常方便。它支持字段验证、表单提交、数据清洗等功能，并且与 Flask 的集成非常紧密。

在本项目中，我们使用 `Flask-WTF` 来处理用户输入的坐标、地址和标签。具体来说：
- **表单**：`CoordinateForm` 是我们为用户输入坐标和标签定义的表单类。表单类继承自 `FlaskForm`，每个字段（如经度、纬度、地址和标签）都使用 WTForms 的字段类型（如 `FloatField` 和 `StringField`）定义。
- **验证**：`Flask-WTF` 提供了字段验证器（如 `DataRequired()`），保证用户提交的表单字段不为空。我们使用它来确保用户输入的经纬度、地址和标签都是有效的。

#### 3.1. **Flask-WTF 表单类 `CoordinateForm`**

`CoordinateForm` 是一个由 Flask-WTF 提供支持的表单类，它继承自 `FlaskForm`，用于处理用户输入并进行表单验证。每个字段都定义了相应的表单组件，并附带了默认的渲染属性（如 `placeholder`）。我们将逐个字段进行分析：

##### 3.1.1 **`lng`：经度字段**
- **字段类型**：`FloatField` 用于输入浮动值，专门用于经度数据的输入。
- **标签与占位符**：通过 `label` 属性为该字段指定中文标签 "经度"；使用 `render_kw={"placeholder": "请输入经度"}` 提供了一个占位符，便于用户理解输入内容。
- **验证**：虽然在代码中没有明确添加验证器，但在实际项目中，`FloatField` 可以结合 `validators` 参数进行进一步的验证。例如，可以添加 `DataRequired()` 来确保经度不为空。

##### 3.1.2 **`lat`：纬度字段**
- **字段类型**：`FloatField` 与经度字段相同，用于输入纬度数据。
- **标签与占位符**：同样的，`label="纬度"` 和占位符 `placeholder="请输入纬度"` 用于用户友好的表单输入界面。

##### 3.1.3 **`address`：地址字段**
- **字段类型**：`StringField` 用于接受地址的文本输入。
- **标签与占位符**：`label="详细地址"` 和 `render_kw={"placeholder": "请输入详细地址"}` 提供了该字段的提示信息。
- **验证**：`StringField` 默认没有进行特殊的验证，但在实际应用中，可以添加如 `DataRequired()` 验证器来确保地址不为空，或者使用 `Length(min=5, max=255)` 来控制地址长度。

##### 3.1.4 **`tag`：标签字段**
- **字段类型**：`StringField` 用于接受用户输入的标签文本，标签可以用来标记地点的类型或分类。
- **标签与占位符**：`label="标签"` 和 `render_kw={"placeholder": "请输入标签"}` 提供了友好的界面提示。
- **验证**：对于标签字段，我们可以添加 `DataRequired()` 和 `Length(min=1, max=100)` 来确保标签不为空且不超过100个字符。

##### 3.1.5 **`submit`：提交按钮**
- **字段类型**：`SubmitField` 用于创建提交按钮，当表单填写完成后，用户点击此按钮提交数据。
- **标签**：`label="添加"` 表示按钮的文本内容。

#### 3.2 **表单验证**
在 Flask-WTF 中，表单验证是其核心特性之一。表单字段可以绑定不同的验证器，确保用户输入符合预期格式和规则。例如，我们可以对经度和纬度字段进行数值范围验证，对地址和标签进行长度限制。

```python
from wtforms.validators import DataRequired, NumberRange, Length

class CoordinateForm(FlaskForm):
    lng = FloatField(
        label="经度", 
        render_kw={"placeholder": "请输入经度"},
        validators=[DataRequired(message="经度不能为空"), 
                    NumberRange(min=-180, max=180, message="经度范围应在-180到180之间")]
    )
    lat = FloatField(
        label="纬度", 
        render_kw={"placeholder": "请输入纬度"},
        validators=[DataRequired(message="纬度不能为空"), 
                    NumberRange(min=-90, max=90, message="纬度范围应在-90到90之间")]
    )
    address = StringField(
        label="详细地址", 
        render_kw={"placeholder": "请输入详细地址"},
        validators=[DataRequired(message="地址不能为空"), 
                    Length(min=5, max=255, message="地址长度应在5到255个字符之间")]
    )
    tag = StringField(
        label="标签", 
        render_kw={"placeholder": "请输入标签"},
        validators=[DataRequired(message="标签不能为空"), 
                    Length(min=1, max=100, message="标签长度应在1到100个字符之间")]
    )
    submit = SubmitField(label="添加")
```

##### 验证器的作用：
- **`DataRequired`**：确保字段不能为空。
- **`NumberRange`**：用于验证经纬度的数值范围，确保经度在-180到180之间，纬度在-90到90之间。
- **`Length`**：验证字符串字段的长度，确保地址和标签的字符数在合理的范围内。

### 4. **表单数据处理**
表单提交后，Flask 会自动进行验证。只有当所有字段都通过验证时，表单数据才会被进一步处理。在控制器（视图函数）中，我们可以通过 `form.validate_on_submit()` 来检查表单是否通过验证，并将数据保存到数据库中。


### 5. **数据库迁移：Flask-Migrate**
`Flask-Migrate` 是一个数据库迁移扩展，它使用 `Alembic` 实现数据库的版本控制。数据库迁移允许开发者在修改数据库模型（如添加新字段或修改表结构）时轻松管理数据库 schema 的变化，而无需手动更改数据库结构。

在本项目中，我们使用 `Flask-Migrate` 来管理数据库的迁移操作：
- 每次我们修改 `Location` 模型时，Flask-Migrate 会生成迁移脚本，并允许我们轻松地执行迁移来更新数据库。
- 使用 `flask db migrate` 命令生成迁移脚本，使用 `flask db upgrade` 来应用迁移脚本更新数据库。

### 6. **日志功能**
项目中使用了 Python 的内置 `logging` 模块来记录日志信息。日志帮助我们跟踪应用程序的运行状态，特别是在调试和出错时非常有用。

在项目中，日志的应用包括：
- 记录数据库操作，例如成功提交新地点记录时的日志。
- 捕获数据库操作中的异常，如果提交数据到数据库失败，应用会回滚操作并记录错误日志。
- 配置日志输出格式，使得每条日志都包含时间戳、日志级别、消息等信息。

### 7. **Baidu Map API：地图显示**
在前端页面中，我们集成了百度地图 API 来显示地点的经纬度信息，并在地图上标记这些地点。百度地图的使用：
- 在 `map.html` 中，我们加载百度地图 API，使用 JavaScript API 来初始化地图。
- 当页面加载时，后端传递给前端所有地点的坐标信息，前端通过 JavaScript 动态创建标记，并将其显示在地图上。
- 每个标记都可以点击，显示该地点的详细信息（如地址和标签）。

### 8. **前端展示与用户交互**
前端部分使用了 `HTML` 和 `Bootstrap` 来构建用户界面：
- 页面加载时，用户可以查看地图以及地图上所有已标记的地点。
- 用户通过表单输入经度、纬度、地址和标签来提交新地点。表单提交后，数据会被传递给后端进行处理，并保存到数据库中。
- 使用 `Bootstrap` 提供的模态框来显示一个弹出表单，使用户能够方便地添加新的地点。
