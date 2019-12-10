import pandas as pd
import chardet
from flask import jsonify, request
from flask_restful import Resource
from fuzzywuzzy import fuzz

from src.client.tenant import get_tenant_data


def match_attributes(match_row, attr_key, attr_values):
    key_match_ratio = fuzz.ratio(match_row['attributeKey'], attr_key)
    matched_attr_key = None
    matched_attr_values = []

    if key_match_ratio > 50:
        for attr_val in attr_values:
            matched_values = set()
            for match_attr_val in match_row['attributeValues']:
                val_match_ratio = fuzz.ratio(match_attr_val['value'], attr_val)
                for sub_str in match_attr_val['value'].split():
                    sub_match_ratio = fuzz.ratio(sub_str, attr_val)
                    if sub_match_ratio == 100:
                        matched_values.add(match_attr_val['value'])
                matched_attr_key = match_row['attributeKey']
                if attr_val.isnumeric() and val_match_ratio == 100 or attr_val.isalpha() and val_match_ratio > 70:
                    matched_values.add(match_attr_val['value'])
            matched_attr_values.append({
                'attrValue': attr_val,
                'matchedAttrData': list(matched_values)
            })
        return {
            'matchedAttrKey': matched_attr_key,
            'matchedAttrValue': matched_attr_values
        }


def translate_scrape_data(csv):
    with open(csv, 'rb') as f:
        # Join binary lines for specified number of lines
        raw_data = b''.join([f.readline() for _ in range(20)])
    encoding = chardet.detect(raw_data)["encoding"]

    json_data = pd.read_csv(csv, encoding=encoding)

    return json_data


class Process(Resource):

    def post(self):
        body = request.json
        tenant_data = get_tenant_data()
        attr_key = body.get('attrKey')
        attr_values = body.get('attrValues')
        tenant_df = pd.DataFrame(tenant_data)
        response = []
        for index, row in tenant_df.iterrows():
            match_data = match_attributes(row, attr_key, attr_values)
            if match_data:
                response.append(match_data)
        return jsonify({
            'processedData': response,
            'status': 200
        })
