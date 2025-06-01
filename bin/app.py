import os
import re

from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, DateField, RadioField, BooleanField, FieldList, FormField, HiddenField, SubmitField

from common import const, sql_shared_service
from app_common import app_shared_service
from mailsearch import search_message, search_settings, models


root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
bin_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# app = Flask(__name__, template_folder=os.path.join(bin_dir, 'slacksearch'), static_folder=os.path.join(bin_dir, 'slacksearch', 'static'))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

class CheckboxItemForm(Form):
    """
    チェックボックス用Form
    """
    checked = BooleanField()
    label = StringField()
    item_id = HiddenField()


class MailSearchForm(FlaskForm):
    """
    検索画面用Form
    """
    search_val = StringField(label='検索文字列')
    search_type = RadioField('search_type_and', choices=[
        ('01', 'AND検索'), ('02', 'OR検索')
    ])
    is_target_title = BooleanField(label='件名')
    is_target_body = BooleanField(label='本文')
    is_target_receive = BooleanField(label='受信メール')
    is_target_send = BooleanField(label='送信メール')
    search_from_date = DateField(label='期間')
    search_to_date = DateField(label='')

    sender_input = StringField(label='')
    sender_list = FieldList(FormField(CheckboxItemForm), min_entries=0)
    folder_list = FieldList(FormField(CheckboxItemForm), min_entries=0)
    to_input = StringField(label='')
    to_list = FieldList(FormField(CheckboxItemForm), min_entries=0)
    sent_folder_list = FieldList(FormField(CheckboxItemForm), min_entries=0)

    search_button = SubmitField('検索', render_kw={'style': 'width: 7em; height: 3em'})


class MailSearchResultForm(FlaskForm):
    """
    検索結果画面用Form
    """
    search_val = HiddenField()
    data_count = StringField()
    entry_id = HiddenField()
    store_id = HiddenField()


class MailSearchDetailForm(FlaskForm):
    """
    詳細画面用Form
    """
    search_val = HiddenField()
    received = StringField('送信日')
    folder_path = StringField('受信ボックス')
    sender = StringField('FROM')
    to_email = StringField('TO')
    cc_email = StringField('CC')
    subject = StringField('件名')
    body = TextAreaField('本文')


class SettingsForm(FlaskForm):
    """
    検索設定画面Form
    """
    regist_button = SubmitField('登録', render_kw={'style': 'width: 7em; height: 3em'})


@app.route('/index')
def index():
    """
    初期表示

    Returns:

    """

    form = MailSearchForm()
    # 検索タイプ
    form.search_type.data = '01'
    # 件名/本文
    form.is_target_title.data = True
    form.is_target_body.data = True
    # 検索場所
    form.is_target_receive.data = True
    with sql_shared_service.get_connection(root_dir) as conn:
        # 差出人
        sender_list = search_message.get_sender_list(conn)
        for data in sender_list:
            entry = form.sender_list.append_entry()
            entry.label.data = f"{data['display_name']} ({app_shared_service.extract_domain(data['email_address'])})"
            entry.item_id.data = data['email_address']
            if data['is_checked']:
                entry.checked.data = True
        # 受信フォルダ
        folder_list = search_message.get_folder_list(conn, const.INBOX)
        for data in folder_list:
            entry = form.folder_list.append_entry()
            entry.label.data = data['folder_path']
            entry.item_id.data = data['folder_id']
            if data['is_target']:
                entry.checked.data = True
        # 送信済フォルダ
        sent_folder_list = search_message.get_folder_list(conn, const.SENT_BOX)
        for data in sent_folder_list:
            entry = form.sent_folder_list.append_entry()
            entry.label.data = data['folder_path']
            entry.item_id.data = data['folder_id']
            if data['is_target']:
                entry.checked.data = True

    return render_template('index.html', form = form)


@app.route('/search', methods=['POST'])
def search():
    """
    検索

    Returns:

    """
    form = MailSearchForm(request.form)
    model = _convert_search_model(form)

    with sql_shared_service.get_connection(root_dir) as conn:
        result_list = search_message.search(conn, model)
    # print(result_list)

    result_form = MailSearchResultForm()
    result_form.search_val = form.search_val
    result_form.data_count.data = f'{len(result_list):,}'

    return render_template('result.html', form=result_form, result_list=result_list)


@app.route('/detail', methods=['POST'])
def detail():
    """
    詳細

    Returns:

    """
    form = MailSearchResultForm(request.form)
    model = _convert_detail_model(form)
    with sql_shared_service.get_connection(root_dir) as conn:
        result = search_message.get_detail(conn, model)

    detail_form = MailSearchDetailForm()
    detail_form.received.data = result.received
    detail_form.folder_path.data = result.folder_path
    detail_form.sender.data = result.sender if result.sender == result.sender_name else f'{result.sender_name}<{result.sender}>'
    detail_form.to_email.data = result.to_email
    detail_form.cc_email.data = result.cc_email
    detail_form.subject.data = result.subject
    detail_form.body.data = result.body

    return render_template('detail.html', form=detail_form)


@app.route('/settings')
def index_settings():
    form = SettingsForm()

    with sql_shared_service.get_connection(root_dir) as conn:
        folder_list = search_settings.get_folder_list(conn)
        sender_list = search_settings.get_sender_list(conn)

    return render_template('indexSettings.html', form=form, folder_list=folder_list, sender_list=sender_list)


@app.route('/registSettings', methods=['POST'])
def regist_settings():
    """
    検索設定登録

    Returns:

    """
    is_target_selected = request.form.getlist('is_target')
    is_sender_display_selected = request.form.getlist('is_sender_display')
    is_sender_checked_selected = request.form.getlist('is_sender_checked')

    # 登録
    with sql_shared_service.get_connection(root_dir) as conn:
        search_settings.regist(conn, is_target_selected, is_sender_display_selected, is_sender_checked_selected)

    return redirect(url_for('index_settings'))


def _convert_search_model(form: MailSearchForm) -> models.MailSearchModel:
    """
    検索用モデルへマッピング

    Args:
        form:

    Returns:

    """
    return models.MailSearchModel(
        form.search_val.data,
        re.split(r'[ 　]+', form.search_val.data) if form.search_val.data else [],
        form.search_type.data,
        form.is_target_title.data,
        form.is_target_body.data,
        form.search_from_date.data,
        form.search_to_date.data,
        form.is_target_receive.data,
        form.is_target_send.data,
        [data.strip() for data in form.sender_input.data.split(';')] if form.sender_input.data else None,
        [entry.item_id.data for entry in form.to_list if entry.checked.data],
        [entry.item_id.data for entry in form.sender_list if entry.checked.data],
        [entry.item_id.data for entry in form.folder_list if entry.checked.data],
        [entry.item_id.data for entry in form.sent_folder_list if entry.checked.data],
    )

def _convert_detail_model(form: MailSearchResultForm) -> models.MailDetailModel:
    """
    詳細用モデルへマッピング

    Args:
        form:

    Returns:

    """
    return models.MailDetailModel(
        form.entry_id.data,
        form.store_id.data,
        form.search_val.data,
        re.split(r'[ 　]+', form.search_val.data) if form.search_val.data else [],
    )


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5101, debug=True)
