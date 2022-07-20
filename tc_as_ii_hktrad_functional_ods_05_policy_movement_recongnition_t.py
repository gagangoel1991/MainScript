import FW.Initialize.initialize_global_variables as iniVar
from UDFs.project_config import project_setup_paths as psp
import FW.Compare_Report.compare_report as cp
import FW.FW_Lib_Connect as dataConnection
import time, os, sys, threading
from FW.FW_tags import tags
from FW.FW_individual_script_runner import run_individual_script

#####################################################################################################################
@tags('functional', 'policy_movement_recognition_t','hktrad','ods')
def test_main(test_name=''):
    psp.Globalinitialize()

    ls_refCols = ['ods_coverage_id']
    pq_coverage_agreement_t='indv_ins_bkp.coverage_agreement_t_q42021_0614'
    pq_contract_t = 'public.IFRS17_CONTRACT_T_Q42020_PRE'
    transaction_reporting_date='2021-03-31'
    src_sql = """with four_transaction_code as (select
ods_coverage_id
,'4' as Transaction_code
,'ON' as movement_indicator
,'New Business' as Movement_Code
,'New Issue' as transaction_description
,'Y' as New_Coverage_flag
from (
select ods_coverage_id from indv_ins.coverage_agreement_t where ifrs17_contract_id in (
select distinct ifrs17_contract_id from indv_ins.coverage_agreement_t
except
select ifrs17_contract_id from public.IFRS17_CONTRACT_T_Q22021) and business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')
except
select ods_coverage_id from public.coverage_agreement_tq22021 where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4'))ss)


,null_transaction_code as (

select 
ods_coverage_id
,null as Transaction_code
,null as movement_indicator
,null as Movement_Code
,null as transaction_description
,'Y' as New_Coverage_flag

from (
select ods_coverage_id from indv_ins.coverage_agreement_t where ifrs17_contract_id in (
select distinct A.ifrs17_contract_id from indv_ins.coverage_agreement_t as A
inner join public.IFRS17_CONTRACT_T_Q22021 as B
on A.ifrs17_contract_id=B.ifrs17_contract_id) and business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')

EXCEPT

select ods_coverage_id from public.coverage_agreement_tq22021 where business_block_code='HK-II-TRAD' )s
Where ods_coverage_id NOT IN (select ods_coverage_id from four_transaction_code))


,used_cov_id as (
select ods_coverage_id from four_transaction_code
UNION ALL
select ods_coverage_id from null_transaction_code
)


,fifteen_transaction_code as (
select
ods_coverage_id 
,'15' as Transaction_code
,'ON' as movement_indicator
,'Reinstatement' as Movement_Code
,'Reinstatement' as transaction_description
,null as New_Coverage_flag

from public.coverage_agreement_tq22021 where ods_coverage_id in (
select ods_coverage_id from indv_ins.coverage_agreement_t where status_code in ('1','2','3','4')
and business_block_code='HK-II-TRAD'
except
select ods_coverage_id from public.coverage_agreement_tq22021 where business_block_code='HK-II-TRAD' and status_code in ('1','2','3','4')) and Status_code in ('B','E')
and ods_coverage_id NOT IN
(
select distinct ods_coverage_id from used_cov_id
))


,used_cov_id_1 as (
select ods_coverage_id from used_cov_id
UNION ALL
select ods_coverage_id from fifteen_transaction_code
)

,death_transaction_code as 
(select CC.ods_coverage_id,BB.TRANSLATION_VALUE from public.coverage_agreement_tq22021 as CC 
Inner join indv_ins.lookup_translation_t as BB
on BB.LOOKUP_VALUE = concat(lpad(CC.SEGMENT_CODE::varchar(4),4,'0'),CC.coverage_plan_id)
and BB.TABLE_ID = 'Group'
AND BB.BUSINESS_ID = '410'
where CC.ods_coverage_id in (
select ods_coverage_id from public.coverage_agreement_tq22021 where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')
except
select ods_coverage_id from indv_ins.coverage_agreement_t where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4'))  and STATUS_CODE = 'D'
and ods_coverage_id NOT IN
(
select distinct ods_coverage_id from used_cov_id_1
))


,used_cov_id_2 as (
select ods_coverage_id from used_cov_id_1
UNION ALL
select ods_coverage_id from death_transaction_code
)

,lapse_transaction_code as (
select 
ods_coverage_id 
,'2' as Transaction_code
,'OFF' as movement_indicator
,'Lapse' as Movement_Code
,'Lapse (including surrenders)' as transaction_description
,null as New_Coverage_flag
from indv_ins.coverage_agreement_t where business_block_code='HK-II-TRAD' and ods_coverage_id in (
select ods_coverage_id from public.coverage_agreement_tq22021 where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')
except
select ods_coverage_id from indv_ins.coverage_agreement_t where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')) and STATUS_CODE = 'B'
and ods_coverage_id NOT IN
(
select distinct ods_coverage_id from used_cov_id_2
))


,used_cov_id_3 as (
select ods_coverage_id from used_cov_id_2
UNION ALL
select ods_coverage_id from lapse_transaction_code
)

,surrender_transaction_code as (
select 
ods_coverage_id 
,'2' as Transaction_code
,'OFF' as movement_indicator
,'Surrendered' as Movement_Code
,'Lapse (including surrenders)' as transaction_description
,null as New_Coverage_flag
from indv_ins.coverage_agreement_t where business_block_code='HK-II-TRAD' and ods_coverage_id in (
select ods_coverage_id from public.coverage_agreement_tq22021 where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')
except
select ods_coverage_id from indv_ins.coverage_agreement_t where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')) and Status_code ='E'
and ods_coverage_id NOT IN
(
select distinct ods_coverage_id from used_cov_id_3
))



,used_cov_id_4 as (
select ods_coverage_id from used_cov_id_3
UNION ALL
select ods_coverage_id from surrender_transaction_code
)

,death_joint_policies_transaction_code as (select CC.ods_coverage_id,BB.TRANSLATION_VALUE from public.coverage_agreement_tq22021 as CC 
left join indv_ins.lookup_translation_t as BB
on BB.LOOKUP_VALUE = concat(lpad(CC.SEGMENT_CODE::varchar(4),4,'0'),CC.coverage_plan_id)
and BB.TABLE_ID = 'Group'
AND BB.BUSINESS_ID = '410'
where CC.ods_coverage_id in (
select ods_coverage_id from public.coverage_agreement_tq22021 where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')
except
select ods_coverage_id from indv_ins.coverage_agreement_t where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')) and Status_code in ('D')
and ods_coverage_id NOT IN
(
select distinct ods_coverage_id from used_cov_id_4
))


,used_cov_id_5 as (
select ods_coverage_id from used_cov_id_4
UNION ALL
select ods_coverage_id from death_joint_policies_transaction_code
)

,miscellaneous_off_transaction_code as (
select 
ods_coverage_id 
,'9' as Transaction_code
,'OFF' as movement_indicator
,'Other Offs' as Movement_Code
,'Miscellaneous Off' as transaction_description
,null as New_Coverage_flag
from indv_ins.coverage_agreement_t where business_block_code='HK-II-TRAD' and ods_coverage_id in (
select ods_coverage_id from public.coverage_agreement_tq22021 where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')
except
select ods_coverage_id from indv_ins.coverage_agreement_t where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')) and Status_code in ('P','R','S','T','W')
and ods_coverage_id NOT IN
(
select distinct ods_coverage_id from used_cov_id_5
))

,used_cov_id_6 as (
select ods_coverage_id from used_cov_id_5
UNION ALL
select ods_coverage_id from miscellaneous_off_transaction_code
)

,miscellaneous_on_transaction_code as (
select 
ods_coverage_id 
,'10' as Transaction_code
,'ON' as movement_indicator
,'Other Ons' as Movement_Code
,'Miscellaneous On' as transaction_description
,null as New_Coverage_flag

from public.coverage_agreement_tq22021 where ods_coverage_id in (
select ods_coverage_id from indv_ins.coverage_agreement_t where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')
except
select ods_coverage_id from public.coverage_agreement_tq22021 where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')) and status_code in ('3', '4', 'D', 'F', 'G', 'H', 'M', 'N', 'R', 'S', 'T', 'W', 'J', 'A', 'P', 'K' )
and ods_coverage_id NOT IN
(
select distinct ods_coverage_id from used_cov_id_6
))

,used_cov_id_7 as (
select ods_coverage_id from used_cov_id_6
UNION ALL
select ods_coverage_id from miscellaneous_on_transaction_code
)

,declined_transaction_code as (
select 
ods_coverage_id 
,'26' as Transaction_code
,'OFF' as movement_indicator
,'Declined' as Movement_Code
,'Not Taken Up' as transaction_description
,null as New_Coverage_flag
from indv_ins.coverage_agreement_t where business_block_code='HK-II-TRAD' and ods_coverage_id in (
select ods_coverage_id from public.coverage_agreement_tq22021 where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')
except
select ods_coverage_id from indv_ins.coverage_agreement_t where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')) and Status_code ='G'
and ods_coverage_id NOT IN
(
select distinct ods_coverage_id from used_cov_id_7))


,used_cov_id_8 as (
select ods_coverage_id from used_cov_id_7
UNION ALL
select ods_coverage_id from miscellaneous_on_transaction_code
)

,not_taken_transaction_code as (
select 
ods_coverage_id 
,'26' as Transaction_code
,'OFF' as movement_indicator
,'Not Taken' as Movement_Code
,'Not Taken Up' as transaction_description
,null as New_Coverage_flag
from indv_ins.coverage_agreement_t where business_block_code='HK-II-TRAD' and ods_coverage_id in (
select ods_coverage_id from public.coverage_agreement_tq22021 where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')
except
select ods_coverage_id from indv_ins.coverage_agreement_t where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')) and Status_code in ('A','N')
and ods_coverage_id NOT IN
(
select distinct ods_coverage_id from used_cov_id_8
))


,used_cov_id_9 as (
select ods_coverage_id from used_cov_id_8
UNION ALL
select ods_coverage_id from not_taken_transaction_code
)

,maturity_transaction_code as (
select 
ods_coverage_id 
,NULL as Transaction_code
,NULL as movement_indicator
,'Maturity' AS Movement_Code
,NULL as transaction_description
,null as New_Coverage_flag
from indv_ins.coverage_agreement_t where business_block_code='HK-II-TRAD' and ods_coverage_id in (
select ods_coverage_id from public.coverage_agreement_tq22021 where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')
except
select ods_coverage_id from indv_ins.coverage_agreement_t where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')) and Status_code in ('F')
and ods_coverage_id NOT IN
(
select distinct ods_coverage_id from used_cov_id_9
))


,used_cov_id_10 as (
select ods_coverage_id from used_cov_id_9
UNION ALL
select ods_coverage_id from maturity_transaction_code
)

,expiry_transaction_code as (
select 
ods_coverage_id 
,NULL as Transaction_code
,NULL as movement_indicator
,'Expired' AS Movement_Code
,NULL as transaction_description
,null as New_Coverage_flag
from indv_ins.coverage_agreement_t where business_block_code='HK-II-TRAD' and ods_coverage_id in (
select ods_coverage_id from public.coverage_agreement_tq22021 where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')
except
select ods_coverage_id from indv_ins.coverage_agreement_t where business_block_code='HK-II-TRAD' and Status_code in ('1','2','3','4')) and Status_code in ('H')
and ods_coverage_id NOT IN
(
select distinct ods_coverage_id from used_cov_id_10
))

select
A.ods_policy_id
,A.POLICY_NUMBER_TEXT
,A.BUSINESS_BLOCK_CODE
,A.BUSINESS_UNIT_KEY
,A.admin_system_code
,B.STATUS_CODE as previous_quarter_status_code
,B.STATUS_EFFECTIVE_DATE as previous_quarter_status_effective_date
,A.STATUS_CODE 
,A.STATUS_EFFECTIVE_DATE
,A.STATUS_EFFECTIVE_DATE as Transaction_effective_date
,'2021-09-30' as transaction_reporting_date
,'Y' as control_framework_validated_flag
,mainlookuptable.*
,null as issue_country_code,
null as insurance_type_code,
null as supplementary_benefit_code,
null as segment_id,
null as current_month_status_code,
null as previous_month_status_code,
null as issue_date,
null as current_month_maturity_expiry_date,
null as status_process_date,
null as reporting_date,
null as previous_month_maturity_expiry_date,
null as plan_id,
null as inforce_tracking_code,
null as source_policy_id

from
(
select * from four_transaction_code --10947
union all 
select * from null_transaction_code
union all 
select * from fifteen_transaction_code
union all 
select * from lapse_transaction_code
union all
select * from surrender_transaction_code
union all
select * from not_taken_transaction_code
union all
select * from miscellaneous_off_transaction_code
union all
select * from miscellaneous_on_transaction_code
union all
select * from declined_transaction_code
union all
select * from maturity_transaction_code
union all
select * from expiry_transaction_code
union all

select
FF.ods_coverage_id
,'3' as Transaction_code
,'OFF' as movement_indicator
,'Death' as Movement_Code
,'Other Benefit (with decrement)' as transaction_description
,null as New_Coverage_flag
from indv_ins.coverage_agreement_t as FF
inner join  death_transaction_code as TT
on FF.ods_coverage_id=TT.ods_coverage_id 
where FF.status_code='D' and 
TT.TRANSLATION_VALUE='Group 1'


union all

select
FF.ods_coverage_id
,'1' as Transaction_code
,'OFF' as movement_indicator
,'Death' as Movement_Code
,'Other Benefit (with decrement)' as transaction_description
,null as New_Coverage_flag
from indv_ins.coverage_agreement_t as FF
inner join  death_transaction_code as TT
on FF.ods_coverage_id=TT.ods_coverage_id
where  FF.status_code='D' and 
TT.TRANSLATION_VALUE='Group 2'

union all

select
FF.ods_coverage_id
,'3' as Transaction_code
,'OFF' as movement_indicator
,'Death' as Movement_Code
,'Morbidity (decrementing)' as transaction_description
,null as New_Coverage_flag
from indv_ins.coverage_agreement_t as FF
inner join  death_transaction_code as TT
on FF.ods_coverage_id=TT.ods_coverage_id where  FF.status_code in ('J','K') and TT.TRANSLATION_VALUE is null

union all

select
FF.ods_coverage_id
,'1' as Transaction_code
,'OFF' as movement_indicator
,'Morbidity (decrementing)' as Movement_Code
,'Death (both lives for joint policies)' as transaction_description
,null as New_Coverage_flag
from indv_ins.coverage_agreement_t as FF
inner join death_joint_policies_transaction_code as TT
on FF.ods_coverage_id=TT.ods_coverage_id where  FF.status_code in ('J','K') and TT.TRANSLATION_VALUE='Group 1'

union all

select
FF.ods_coverage_id
,'1' as Transaction_code
,'OFF' as movement_indicator
,'Death' as Movement_Code
,'Death (both lives for joint policies)' as transaction_description
,null as New_Coverage_flag
from indv_ins.coverage_agreement_t as FF
inner join  death_joint_policies_transaction_code as TT
on FF.ods_coverage_id=TT.ods_coverage_id where  FF.status_code in ('D') and TT.TRANSLATION_VALUE is null) mainlookuptable
LEFT join indv_ins.coverage_agreement_t as A
on mainlookuptable.ods_coverage_id=A.ods_coverage_id
LEFT join public.coverage_agreement_tq22021 as B
on mainlookuptable.ods_coverage_id=B.ods_coverage_id"""

    trg_sql = """
select
ods_policy_id
,policy_number_text
,business_block_code
,business_unit_key
,admin_system_code
,previous_quarter_status_code
,previous_quarter_status_effective_date
,status_code
,status_effective_date
,transaction_effective_date
,transaction_reporting_date
,control_framework_validated_flag
,ods_coverage_id
,transaction_code
,movement_indicator
,movement_code
,transaction_description
,new_coverage_flag
,issue_country_code
,insurance_type_code
,supplementary_benefit_code
,segment_id
,current_month_status_code
,previous_month_status_code
,issue_date
,current_month_maturity_expiry_date
,status_process_date
,reporting_date
,previous_month_maturity_expiry_date
,plan_id
,inforce_tracking_code
,source_policy_id
from indv_ins.policy_movement_recognition_t

            """

    # fetch data
    df_src = dataConnection.read_PostgreSQL_to_df_Source(r"Acturial_Connections\aods_hk_indv_ins_sit", src_sql)
    df_trg = dataConnection.read_PostgreSQL_to_df_Target(r"Acturial_Connections\aods_hk_indv_ins_sit", trg_sql)
    ls_allCols_to_validate=df_src.columns.values
    # validate results
    cp.compare([df_src, ls_refCols, ls_allCols_to_validate], [df_trg, ls_refCols, ls_allCols_to_validate])





#####################################################################################################################
# generate reports
def test_reporting(rptCnt=1, testName=None, Error=None, totaltestsCount=1):
    cp.prepareReport(rptCnt, testName, Error, totaltestsCount)


if __name__ == "__main__":
    dry_run = False
    current_test_name = os.path.basename(sys.argv[0])
    run_individual_script(test_main, test_reporting, current_test_name, dry_run=dry_run, verbose_debug=False)


