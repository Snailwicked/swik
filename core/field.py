#!/usr/bin/env python

from lxml import etree
import re
from typing import Union
from copy import deepcopy


class NothingMatchedError(Exception):
    pass


class BaseField(object):
    """
    BaseField class
    """

    def __init__(self, default: str = '', many: bool = False):
        """
        Init BaseField class
        url: http://lxml.de/index.html
        :param css_select: css select http://lxml.de/cssselect.html
        :param xpath_select: http://www.w3school.com.cn/xpath/index.asp
        :param default: default value
        """
        self.default = default
        self.many =many


    def extract(self, *args, **kwargs):
        raise NotImplementedError('extract is not implemented.')

class _LxmlElementField(BaseField):


    def __init__(self, css_select=None, xpath_select=None, default: str = None, many: bool = False):
        """
        :param css_select: css select http://lxml.de/cssselect.html
        :param xpath_select: http://www.w3school.com.cn/xpath/index.asp
        :param default: inherit
        :param many: inherit
        """
        super(_LxmlElementField, self).__init__(default=default, many=many)
        self.css_select = css_select
        self.xpath_select = xpath_select


    def _get_elements(self, *, html_etree: etree._Element):
        if self.css_select:
            elements = html_etree.cssselect(self.css_select)
        elif self.xpath_select:
            elements = html_etree.xpath(self.xpath_select)
        else:
            raise ValueError('%s field: css_select or xpath_select is expected' % self.__class__.__name__)

        if not self.many:
            elements = elements[:1]
        return elements

    def _parse_element(self, element):
        raise NotImplementedError

    def extract(self, *, html_etree: etree._Element, is_source: bool = False):
        elements = self._get_elements(html_etree=html_etree)
        if is_source:
            return elements if self.many else elements[0]

        if elements:
            results = [self._parse_element(element) for element in elements]
        elif self.default is None:
            raise NothingMatchedError(self.css_select or self.xpath_select)
        else:
            results = [self.default]
        return results if self.many else results[0]



class TextField(_LxmlElementField):

    def _parse_element(self, element):
        strings = [node.strip() for node in element.itertext()]
        string = ''.join(strings)
        return string if string else self.default



class AttrField(_LxmlElementField):
    def __init__(self, attr, css_select=None, xpath_select=None, default='', many: bool = False):
        super(AttrField, self).__init__(
            css_select=css_select, xpath_select=xpath_select, default=default, many=many)
        self.attr = attr

    def _parse_element(self, element):
        return element.get(self.attr, self.default)


class HtmlField(_LxmlElementField):
    """
    This field is used to get raw html code.
    """

    def _parse_element(self, element):
        return etree.tostring(element).decode(encoding='utf-8')

class RegexField(BaseField):
    """
    This field is used to get raw html code by regular expression.
    RegexField uses standard library `re` inner, that is to say it has a better performance than _LxmlElementField.
    """

    def __init__(self, re_select: str, default: str = '', many: bool = False):
        super(RegexField, self).__init__(default=default, many=many)
        assert isinstance(re_select, str)
        self._re_select = re_select
        self._re_object = re.compile(self._re_select)

    def _parse_match(self, match):
        """
        If there is a group dict, return the dict;
            even if there's only one value in the dict, return a dictionary;
        If there is a group in match, return the group;
            if there is only one value in the group, return the value;
        if there has no group, return the whole matched string;
        if there are many groups, return a tuple;
        :param match:
        :return:
        """
        if not match:
            if self.default:
                return self.default
            else:
                raise NothingMatchedError('Nothing matched: ' + self._re_select)
        else:
            string = match.group()
            groups = match.groups()
            group_dict = match.groupdict()
            if group_dict:
                return group_dict
            if groups:
                return groups[0] if len(groups) == 1 else groups
            return string

    def extract(self, html: Union[str, etree._Element]):
        if isinstance(html, etree._Element):
            html = etree.tostring(html).decode(encoding='utf-8')
        if self.many:
            matches = self._re_object.finditer(html)
            return [self._parse_match(match) for match in matches]
        else:
            match = self._re_object.search(html)
            return self._parse_match(match)