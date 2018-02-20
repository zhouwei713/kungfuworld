'''
Created on 20171025

@author: zhou
'''
#coding=utf-8

import re

def escape_text(txt):
    return txt.replace('<', '&lt;').replace('>', '&gt;')

def make_re_url():
    url = ''
    return re.compile(url, re.VERBOSE | re.MULTILINE)

RE_URL = make_re_url()

def linkify(txt,
            shorten = True,
            target_blank = False,
            require_protocol = False,
            permitted_protocols = ["http", "https"],
            local_domain = None):
    """Converts plain txt into HTML with links. back ported from tornado 2.0
    For example: ``linkify("Hello http://tornadoweb.org!")`` would return
    ``Hello <a href="http://tornadoweb.org">http://tornadoweb.org</a>!``
    Parameters:
    shorten: Long urls will be shortened for display.
    extra_params: Extra txt to include in the link tag,
        e.g. linkify(txt, extra_params='rel="nofollow" class="external"')
    require_protocol: Only linkify urls which include a protocol. If this is
        False, urls such as www.facebook.com will also be linkified.
    permitted_protocols: List (or set) of protocols which should be linkified,
        e.g. linkify(txt, permitted_protocols=["http", "ftp", "mailto"]).
        It is very unsafe to include protocols such as "javascript".
    local_domain: domain link
    """

    if txt is None or not txt.strip():
        return txt
    extra_params = ' rel="nofollow"'

    def make_link(m):
        tb = target_blank
        url = m.group(1)
        proto = m.group(2)
        if require_protocol and not proto:
            return url  # not protocol, no linkify

        if proto and proto not in permitted_protocols:
            return url  # bad protocol, no linkify

        href = m.group(1)
        #href = xhtml_unescape(href).strip()
        if not proto:
            href = "http://" + href   # no proto specified, use http

        params = extra_params
        if proto:
            proto_len = len(proto) + 1 + len(m.group(3) or "")  # +1 for :
        else:
            proto_len = 0

        parts = url[proto_len:].split("/")

        proto_part = url[:proto_len] if proto != 'http' else ''
        host_part = parts[0]

        if host_part.startswith('www.'):
            host_part = '.'.join(host_part.split('.')[1:]) # add extra idnetification for external link
        if not local_domain or not host_part.endswith(local_domain):
            params  += ' class="external" '
            tb = True

        if tb:
            params  += 'target="_blank"'

        # clip long urls. max_len is just an approximation
        max_len = 30
        if shorten and len(url) > max_len:
            before_clip = url[proto_len:]
            url = proto_part + host_part
            #if len(parts) > 2:
                # Grab the whole host part plus the first bit of the path
                # The path is usually not that interesting once shortened
                # (no more slug, etc), so it really just provides a little
                # extra indication of shortening.
            for n,p in enumerate(parts[1:]):
                if n:
                    cut = 6
                else:
                    cut = 8
                url += '/' + p[:cut].split('?')[0].split('.')[0]
                if len(p) < 4:
                    continue
                break
                #url = proto_part + host_part  + "/" + \
                        #parts[1][:8].split('?')[0].split('.')[0]

            if len(url) > max_len * 1.5:  # still too long
                url = url[:max_len]

            if url != before_clip:
                amp = url.rfind('&')
                # avoid splitting html char entities
                if amp > max_len - 5:
                    url = url[:amp]
                url += "..."

                if len(url) >= len(before_clip):
                    url = before_clip
                else:
                    # full url is visible on mouse-over (for those who don't
                    # have a status bar, such as Safari by default)
                    params += ' title="%s"' % href

        return u'<a href="%s"%s>%s</a>' % (href, params, url)

    return RE_URL.sub(make_link, txt)

if __name__ == '__main__':
    txt = 'have a link test www.zhihu.com/question/19550224?noti_id=123 how about?'
    txt1 = 'hello http://tornadoweb.org!'
    print linkify(txt)