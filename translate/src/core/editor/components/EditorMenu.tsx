import { Localized } from '@fluent/react';
import React from 'react';
import { useClearEditor } from '~/context/Editor';

import { useSelectedEntity } from '~/core/entities/hooks';
import * as user from '~/core/user';
import { saveSetting } from '~/core/user/actions';
import { useAppDispatch, useAppSelector } from '~/hooks';
import { UnsavedChangesPopup } from '~/modules/unsavedchanges/components/UnsavedChangesPopup';
import { TranslationLength } from './TranslationLength';
import { useCopyOriginalIntoEditor } from '../hooks/useCopyOriginalIntoEditor';

import { EditorMainAction } from './EditorMainAction';
import './EditorMenu.css';
import { EditorSettings } from './EditorSettings';
import { FailedChecks } from './FailedChecks';
import { FtlSwitch } from './FtlSwitch';
import { KeyboardShortcuts } from './KeyboardShortcuts';

/**
 * Shows a menu bar used to control the Editor.
 *
 * If the user is not authenticated, shows a login button.
 * If the entity is read-only, shows a read-only notification.
 * Otherise, shows the various tools to control the editor.
 */
export function EditorMenu(): React.ReactElement<'menu'> {
  return (
    <menu className='editor-menu'>
      <FtlSwitch />
      <FailedChecks />
      <UnsavedChangesPopup />
      <MenuContent />
    </menu>
  );
}

function MenuContent() {
  const clearEditor = useClearEditor();
  const copyOriginalIntoEditor = useCopyOriginalIntoEditor();
  const dispatch = useAppDispatch();
  const entity = useSelectedEntity();
  const userState = useAppSelector((state) => state.user);

  if (!userState.isAuthenticated) {
    return (
      <Localized
        id='editor-EditorMenu--sign-in-to-translate'
        elems={{ a: <user.SignInLink url={userState.signInURL} /> }}
      >
        <p className='banner'>{'<a>Sign in</a> to translate.'}</p>
      </Localized>
    );
  }

  if (entity?.readonly) {
    return (
      <Localized id='editor-EditorMenu--read-only-localization'>
        <p className='banner'>This is a read-only localization.</p>
      </Localized>
    );
  }

  function updateSetting(setting: keyof user.Settings, value: boolean) {
    dispatch(saveSetting(setting, value, userState.username));
  }

  return (
    <>
      <EditorSettings
        settings={userState.settings}
        updateSetting={updateSetting}
      />
      <KeyboardShortcuts />
      <TranslationLength />
      <div className='actions'>
        <Localized id='editor-EditorMenu--button-copy' attrs={{ title: true }}>
          <button
            className='action-copy'
            onClick={copyOriginalIntoEditor}
            title='Copy From Source (Ctrl + Shift + C)'
          >
            COPY
          </button>
        </Localized>
        <Localized id='editor-EditorMenu--button-clear' attrs={{ title: true }}>
          <button
            className='action-clear'
            onClick={clearEditor}
            title='Clear Translation (Ctrl + Shift + Backspace)'
          >
            CLEAR
          </button>
        </Localized>
        <EditorMainAction />
      </div>
    </>
  );
}