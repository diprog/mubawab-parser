get_phone_number_ajax = '''
    async (request_url, encryptedPhone, zoneCreated, sourceHiddenBox, landingHiddenBox, adIdLead, promotionIdLead) => {
        const body = {
            encryptedPhone: encryptedPhone,
            source: sourceHiddenBox,
            landingPage: landingHiddenBox,
            zoneCreated: zoneCreated
        };
        if (adIdLead) {
            body['adId'] = adIdLead;
        }
        if (promotionIdLead) {
            body['promotionId'] = promotionIdLead;
        }
        var resp = await doAjaxPOSTAsync(request_url, getDataToSend(null, body), '212312321');
        return resp.value;
    }
'''

get_map_coords = '''
    (serviceUrl, type, id) => {
        serviceUrl += '?id=' + id + '&type=' + type;
        const response = doAjaxPOST(serviceUrl);
        const center = iuwy(dfse(response.split('^')[1]));
        if (center != 0) {
            const pos = center.replace('(', '').replace(')', '').split(',');
            return pos;
        }
    }
'''