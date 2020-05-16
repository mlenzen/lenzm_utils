# Template Filters

@bp.app_template_filter('cond_classes')
def filter_cond_classes(v):
    """Conditionally build a list of classes.

    For example, filter_cond_classes({'a': True, 'b': False, 'c': True})
    returns 'a b'.
    """
    classes = [class_ for class_, cond in v.items() if cond]
    return ' '.join(classes)


@bp.app_template_filter('url_quote')
def filter_url_quote(value):
    return urllib.parse.quote(value)


@bp.app_template_filter('int_comma')
def format_int_comma(value):
    if value is None:
        return ''
    return '{:,}'.format(int(round(value)))


@bp.app_template_filter('date')
def filter_date(d, format='%Y-%m-%d'):
    if not d:
        return 'unknown'
    readable = d.strftime(format)
    return Markup('<time datetime={machine}>{readable}</time>'.format(
        readable=readable,
        machine=d.isoformat(),
    ))


@bp.app_template_filter('currency')
def filter_currency(value, decimals=True):
    if not value and value != 0:
        return ''
    if decimals:
        return '${:,.2f}'.format(value)
    else:
        return '${:,.0f}'.format(value)


@bp.app_template_filter('accounting')
def filter_accounting(value, decimals=False):
    if not value and value != 0:
        return ''
    if value < 0:
        value = -value
        if decimals:
            return '({:,.2f})'.format(value)
        else:
            return '({:,.0f})'.format(value)
    elif value > 0:
        if decimals:
            return '{:,.2f}'.format(value)
        else:
            return '{:,.0f}'.format(value)
    else:
        return '-'
