# coding=utf-8
from __future__ import division, print_function, unicode_literals

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList


class ChangeListTotals(ChangeList):
    def get_results(self, *args, **kwargs):
        super(ChangeListTotals, self).get_results(*args, **kwargs)
        if hasattr(self.model_admin, 'list_totals'):
            self.aggregations = []
            list_totals = dict(self.model_admin.list_totals)
            for field in self.list_display:
                if field in list_totals:
                    if type(list_totals[field]) != tuple:
                        model_field = field
                        func = list_totals[field]
                        formatter = str
                    else:
                        func, model_field, formatter = list_totals[field]
                    total = formatter(self.result_list.aggregate(agg=func(model_field))['agg'])
                    self.aggregations.append(total)
                else:
                    self.aggregations.append('')


class ModelAdminTotals(admin.ModelAdmin):
    change_list_template = 'admin_totals/change_list_totals.html'

    def get_changelist(self, request, **kwargs):
        return ChangeListTotals
